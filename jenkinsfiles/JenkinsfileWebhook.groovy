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
            
            printContributedVariables: true,
            printPostContent: true,        
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

                    if(prHeadRef != null && (prAction.equals("opened") || prAction.equals("reopened"))) {
                        echo "Clonning code form branch: ${prHeadRef}";
                        // This will label a build with BUILD_NUMBER PR_ACTION:PR_REF, for example: #1 opened: fcd1202 which means build #1 has a PR opened for branch fcd1202
                        currentBuild.displayName = "#${env.BUILD_NUMBER} ${prAction}:${prHeadRef} (test)";
                        build job: 'prancer/basic/prancer-test', parameters: [string(name: 'branch', value: prHeadRef)], wait: false;
                    } else if(environmentVariables.containsKey("PR_HEAD_MERGED") 
                                && environmentVariables.PR_HEAD_MERGED.trim().equals("true")
                                && environmentVariables.containsKey("PR_BASE_REF")
                                && environmentVariables.PR_BASE_REF.trim().contains("master")) {
                        echo "A PR has been merged";
                        currentBuild.displayName = "#${env.BUILD_NUMBER} merge -> ${environmentVariables.PR_BASE_REF}";
                        build job: 'prancer/basic/prancer-release', parameters: [string(name: 'branch', value: prHeadRef)], wait: false;
                    }                    
                }
            }
        }
    }
}
