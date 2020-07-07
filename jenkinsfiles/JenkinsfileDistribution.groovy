pipeline {
    agent {
        label "master"
    }

    parameters {
        string(name: 'branch', defaultValue: 'master', description: 'Branch to release')
    }

    environment {
        PYTHON_DOCKER_IMAGE = "python:3.6"
        PIP_CREDENTIAL_ID = "PIP_CREDENTIAL_ID"
        PIP_TEST_CREDENTIAL_ID = "PIP_TEST_CREDENTIAL_ID"
        DOCKERHUB_CREDENTIAL_ID = "DOCKERHUB_CREDENTIAL_ID"
        DOCKERHUB_IMAGE_NAME = "prancer-basic"
        DOCKERHUB_PUBLIC_REPOSITORY = "https://registry.hub.docker.com/prancer"
        DOCKERHUB_ORG = "prancer"
        GITHUB_USER_AGENT = "Jenkins-client"
        GITHUB_API_TOKEN = "GITHUB_API_TOKEN"
        GITHUB_ORG = "prancer-io" 
        GITHUB_REPO = "cloud-validation-framework"
        ALPINE_DOCKER_IMAGE = "alpine:3.10.2"
    }

    stages {

        stage("Git clone") {
            steps {
                script {
                    git url: "https://github.com/${GITHUB_ORG}/${GITHUB_REPO}.git", branch: branch;
                    setupPyText = readFile file: "setup.py";
                    currentVersionLine = setupPyText.split("\n").find{ element -> element.contains("version=") };
                    currentVersion = currentVersionLine.split("=")[1].replace("'", "").replace("\"", "").replace(",", "").trim();
                    currentVersion = currentVersion.trim().split(" ")[0];
                    currentDirectory = pwd();
                    echo "*** Current version ${currentVersion} from setup.py. ";
                    try {
                        sh "rm dist/*";
                    } catch(e) {
                        echo "Warning: error trying to rm dist/*"
                    }
                }
            }
        }

        stage("Create git tag") {
            steps {
                script {
                    // Create a Git tag using the Git Rest API
                    withCredentials([string(credentialsId: GITHUB_API_TOKEN, variable: 'GITHUB_API_TOKEN_VAR')]) {
                        // Custom Http header for the API
                        customHeader = [[name: 'Authorization', value: "token ${GITHUB_API_TOKEN_VAR}"],
                                        [name: 'User-Agent', value: "token ${GITHUB_USER_AGENT}"]];
                        tag = "V${currentVersion}";
                        // Check If the release already exits
                        apiURL = "https://api.github.com/repos/${GITHUB_ORG}/${GITHUB_REPO}/releases/tags/${tag}";

                        response = httpRequest acceptType: 'APPLICATION_JSON', 
                                            contentType: 'APPLICATION_JSON', 
                                            httpMode: 'GET', 
                                            url: apiURL, 
                                            customHeaders: customHeader,
                                            validResponseCodes: "200,201,400,404";
                        
                        if(response.status == 200 || response.status == 202 || response.status != 404) {
                            error "Error: Release ${tag} is already created. Response status ${response.status}";
                        } 

                        echo "${response.content}";

                        // Create the payload for the release
                        requestBody = "{" +
                                        "\"tag_name\": " + "\"${tag}\"," +
                                        "\"target_commitish\": " + "\"${branch}\"," +
                                        "\"name\": " + "\"${tag}\"," +
                                        "\"body\": " + "\"Release: ${tag}\"," +
                                        "\"draft\": " + "false," +
                                        "\"prerelease\": " + "false" +
                                      "}";

                        echo requestBody
                        // Create the github release definition
                        apiURL = "https://api.github.com/repos/${GITHUB_ORG}/${GITHUB_REPO}/releases";

                        response = httpRequest acceptType: 'APPLICATION_JSON', 
                                            contentType: 'APPLICATION_JSON', 
                                            httpMode: 'POST', 
                                            url: apiURL, 
                                            customHeaders: customHeader,
                                            requestBody: requestBody;

                        responseJsonObject = readJSON text: response.content;
                        
                        // From the response it returns 'upload_url' which is the URL that allow us to upload binaries
                        uploadUrl = responseJsonObject.upload_url.replace("{?name,label}", "");
                        echo "*** Upload URL ${uploadUrl}";
                        echo "${response}";
                    }                   
                }
            }
        }

        stage("Build release") {

            agent {
                docker {
                    image PYTHON_DOCKER_IMAGE
                    args "-v ${currentDirectory}:${currentDirectory}"
                }
            }

            steps {
                script {
                    sh "cd ${currentDirectory} && python setup.py sdist bdist_wheel";
                }
            }
        }

        stage("Upload assets to github") {
            agent {
                docker {
                    image ALPINE_DOCKER_IMAGE
                    args "-u root -v ${currentDirectory}:${currentDirectory}"
                }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: GITHUB_API_TOKEN, variable: 'GITHUB_API_TOKEN_VAR')]) {
                        // Install tools required in alpine: curl, zip
                        sh "apk add --no-cache curl zip";
                        // Print the size and the name of the files in /dist directory
                        output = sh script: "ls -lt ${currentDirectory}/dist | awk '{print \$5,\$9}'", returnStdout: true;
                        listOfFiles = output.split("\n");
                        listOfFiles.each {
                            lineFile ->
                                if(!lineFile.trim().isEmpty()) {
                                    // Each lineFile might look like this: 66367 file.whl, where 66367 is the size and file.whl the file name
                                    lineFileSplit = lineFile.split(" ");
                                    fileLenght = lineFileSplit[0].trim();
                                    fileName = lineFileSplit[1].trim();
                                    command = "cd ${currentDirectory}/dist && curl -X POST --data-binary @\"${fileName}\" -H \"Content-Length: ${fileLenght}\" -H \"Content-type: application/zip\" -H \"Authorization: token ${GITHUB_API_TOKEN_VAR}\" -H \"User-Agent: ${GITHUB_USER_AGENT}\" ${uploadUrl}?name=${fileName}";
                                    sh command;
                                }                            
                        }                        
                    }
                }
            }
        }

        stage("Push to pypi.org") {
            agent {
                docker {
                    image PYTHON_DOCKER_IMAGE
                    args "-v ${currentDirectory}:${currentDirectory} -u root"
                }
            }

            // Publish artifact in pypi. An account need to be created in this link: https://test.pypi.org/account/register/
            steps {
                script {
                    // Install Twine to distribute application. Reference: https://packaging.python.org/tutorials/packaging-projects/
                    withCredentials([usernamePassword(credentialsId: PIP_CREDENTIAL_ID, passwordVariable: 'pipPassword', usernameVariable: 'pipUser')]) {
                        sh "pip install twine"
                        sh "twine --version"
                        sh "cd ${currentDirectory} && " + 
                           "twine upload dist/* -u ${pipUser} -p ${pipPassword}";
                    }                    
                }
            }
        }

        stage("Push to dockerhub") {
            steps {
                script {
                    docker.withRegistry(DOCKERHUB_PUBLIC_REPOSITORY, DOCKERHUB_CREDENTIAL_ID) {
                        // This sleep is intended to allow pypi.org some time in order to properly resolve pip install for recent binaries
                        sleep 60;
                        def customImage = docker.build("${DOCKERHUB_ORG}/${DOCKERHUB_IMAGE_NAME}:${currentVersion}", 
                                                       "--build-arg APP_VERSION=${currentVersion} " +
                                                       "-f dockerfiles/Dockerfile .");
                        customImage.push();
                        customImage.push("latest");
                        // Clean image pushed from local registry
                        try {
                            sh "docker image rm ${DOCKERHUB_ORG}/${DOCKERHUB_IMAGE_NAME}:${currentVersion}";
                        } catch(e) {
                            echo "Exception with 'docker image rm' ${e}";
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                echo "*** Sending success notification";
                slackSend color: 'good', message: "cloud-validation-framework [SUCCESS] ${BUILD_URL}";
            }
        }
        failure {
            script {
                echo "*** Sending failure notification"
                slackSend color: 'danger', message: "cloud-validation-framework [FAILURE] ${BUILD_URL}";
            }
        }
    }
}
