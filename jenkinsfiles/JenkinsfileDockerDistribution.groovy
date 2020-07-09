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

        stage("Push to dockerhub") {
            steps {
                script {
                    docker.withRegistry(DOCKERHUB_PUBLIC_REPOSITORY, DOCKERHUB_CREDENTIAL_ID) {
                        // This sleep is intended to allow pypi.org some time in order to properly resolve pip install for recent binaries
                        def customImage = docker.build("${DOCKERHUB_ORG}/${DOCKERHUB_IMAGE_NAME}:${app_version}", 
                                                       "--build-arg APP_VERSION=${app_version} " +
                                                       "-f dockerfiles/Dockerfile .");
                        customImage.push();
                        customImage.push("latest");
                        // Clean image pushed from local registry
                        try {
                            sh "docker image rm ${DOCKERHUB_ORG}/${DOCKERHUB_IMAGE_NAME}:${app_version}";
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
                slackSend color: 'good', message: "[Docker] cloud-validation-framework [SUCCESS] ${BUILD_URL}";
            }
        }
        failure {
            script {
                echo "*** Sending failure notification"
                slackSend color: 'danger', message: "[Docker] cloud-validation-framework [FAILURE] ${BUILD_URL}";
            }
        }
    }
}
