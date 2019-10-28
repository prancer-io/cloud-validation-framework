/*
Job 1 (Test)
after sending the PR (automatic)
    - run test pointing to the branch  with the latest commit for python3.5, 3.6, 3.7:
    1. run unit tests
    2. security scanning of the code (integration with Snyk / Veracode / Sonarquebe)
    3. provision a new container with the framework new code
    4. run a test scenario
    
Manual step:
    Reviewer approves PR
    
Job 2: Release (Manual)
Github sends an event from the PR ->
    * Use Master branch
    Read version from a file (TBD), let's suppose version A.B.C
    Create a tag with the version A.B.C
    Push tag A.B.C
    
    Generate a release
    python setup.py sdist bdist_wheel
    Place the relase generated in a folder easy to reach from Jenkins, localhost:8080/userContent
        With a folder
            prancer/
                releases/
                    X.X.X/
                    A.B.C/
                        files
    push the release to pip
    push the release to github
    build the container and release in dockerhub
    generate new documentations / update the website documentation
    update the code in the test server

Process:
    Developer -> Open a PR from branch "feature"
        Jenkins test job:
            - git clone from "feature" branch
            - Perform testing for Python images python:3.5,python:3.6,python:3.7
            - Perform SNYK code analysis
            - Run test script

    User approves PR from branch "feature"
        Jenkins release job:
            ** Let's assume setup.py contains 1.2.3
            - Pipeline read setup.py file with version 1.2.3 
            - Pipeline verifies tag/release 1.2.3 exists or not
                - If exists
                    throw an error
                - else
                    - create git tag/release
            - Build binaries 'python setup.py sdist bdist_wheel'
            - Attach binaries in dist/* to github release 1.2.3
            - Publish to pypi.org binaries. Using Python 3.6 and twine
            - Publish a Docker image to Dockerhub. Using a base Python 3.6 image and on top of it 'pip install prancer-basic'
            

*/
pipeline {
    agent {
        label "master"
    }

    
    triggers {
        GenericTrigger(
            genericVariables: [
                [
                    key: 'PR_ACTION', 
                    value: '$.action'
                ],
                [
                    key: 'PR_HEAD_REF', 
                    value: '$.pull_request.head.ref'
                ],
                [
                    key: 'PR_HEAD_MERGED', 
                    value: '$.pull_request.merged'
                ],
                [
                    key: 'PR_BASE_REF', 
                    value: '$.pull_request.base.ref'
                ]
            ],
            
            causeString: 'PR ($PR_ACTION):$PR_HEAD_REF',
            
            token: 'prancer-github-pr',
            
            printContributedVariables: false,
            printPostContent: false,        
            silentResponse: true
        )
    }

    stages {
        stage("Git clone") {
            steps {
                script {
                    def environmentVariables = env.getEnvironment();
                    prAction = null;
                    prHeadRef = null;

                    if(environmentVariables.containsKey("PR_ACTION") && environmentVariables.containsKey("PR_HEAD_REF")) {
                        echo "Variable JSON_POST_STR has been injected";
                        prAction = PR_ACTION;
                        prHeadRef = PR_HEAD_REF;
                    } 

                    if(prHeadRef != null && prAction.equals("opened")) {
                        echo "Clonning code form branch: ${prHeadRef}";
                        // This will label a build with BUILD_NUMBER PR_ACTION:PR_REF, for example: #1 opened: fcd1202 which means build #1 has a PR opened for branch fcd1202
                        currentBuild.displayName = "#${env.BUILD_NUMBER} ${prAction}:${prHeadRef}";
                        build job: 'prancer/prancer-test', parameters: [string(name: 'branch', value: prHeadRef)], wait: false;
                    } else if(environmentVariables.containsKey("PR_HEAD_MERGED") 
                                && environmentVariables.PR_HEAD_MERGED 
                                && environmentVariables.containsKey("PR_BASE_REF")
                                && environmentVariables.PR_BASE_REF.trim().contains("master")) {
                        echo "A PR has been merged";
                        currentBuild.displayName = "#${env.BUILD_NUMBER} merge -> ${environmentVariables.PR_BASE_REF}";
                        build job: 'prancer/prancer-release', parameters: [string(name: 'branch', value: prHeadRef)], wait: false;
                    }                    
                }
            }
        }
    }
}