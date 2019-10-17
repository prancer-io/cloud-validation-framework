pipeline {
    agent {
        label "master"
    }

    parameters {
        string(name: 'branch', defaultValue: 'master', description: 'Branch to build')
    }

    environment {
        GIT_CLOUD_VALIDATION_FRAMEWORK = "https://github.com/prancer-io/cloud-validation-framework.git"
        PYTHON_DOCKER_IMAGES_TEST = "python:3.5,python:3.6,python:3.7"
        SNYK_DOCKER_IMAGE = "snyk/snyk-cli:python-3"
    }

    stages {
        stage("Git clone") {
            steps {
                script {
                    git url: GIT_CLOUD_VALIDATION_FRAMEWORK, branch: branch;                    
                    currentDir = pwd();
                    currentBuild.displayName = "#${env.BUILD_NUMBER} branch: ${branch}";
                }
            }
        }

        stage("Unit testing Python") {
            steps {
                script {
                    def parallelTesting = [:];
                    // Create an array of docker images to iterate
                    def dockerImages = PYTHON_DOCKER_IMAGES_TEST.split(",");
                    
                    dockerImages.each {
                        dockerImage ->
                            try {
                                docker.image(dockerImage).inside("-e PYTHONPATH=${currentDir}/src -u root") {       
                                    sh "pip3 install attrs==19.1.0"                            
                                    sh "pip3 install -r requirements.txt";
                                    sh "py.test --cov=processor tests/processor --cov-report term-missing";                             
                                }
                            } catch(e) {
                                error "*** Error during unit testing in Docker image ${dockerImage}. Exception: ${e}"
                            }
                    }
                }
            }
        }

        stage("Code analysis") {
            steps {
                script {
                    // Perform code security analysis using snyk docker image
                    withCredentials([string(credentialsId: 'SNYK_CREDENTIAL_TOKEN', variable: 'SNYK_CREDENTIAL_TOKEN')]) {
                        sh "docker run -e \"SNYK_TOKEN=${SNYK_CREDENTIAL_TOKEN}\" -e \"MONITOR=true\" -v \"${currentDir}:/project\" ${SNYK_DOCKER_IMAGE} monitor --command=python3 --project-name=cloud-validation-framework";
                    }
                }
            }
        }

        stage("Run test") {
            steps {
                script {
                    echo "Running test script"
                }
            }
        }
    }

}