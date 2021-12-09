
COMPLIANCES = [{
    "masterTestId":"SENSITIVE_EXTENSION_TEST",
    "masterSnapshotId" : [
        "ALL"
    ],
    "type":"python",
    "rule":"file(sensitive_extension.py)",
    "evals":[
        {
            "id":"PR-COM-SEN-EXT-001",
            "eval":"data.rule.sensitive_extensions",
            "message":"data.rule.sensitive_extensions_err",
            "remediationDescription":"you need to add these extensions to your .gitignore file to prevent them from checking in to your repository. these files need to be moved securely to a vault to be managed securely and then referenced in your code",
            "remediationFunction":""
        }
    ],
    "severity":"Medium",
    "title":"Sensitive files should not be checked into the git repo",
    "description":"Certain file types contain sensitive information and should not be checked into the git repositories. You need to move these files to a vault and reference them from your code. Prancer checks for the following file types to make sure they are not in the repo:<br>*.PFX or *.P12 - Personal Information Exchange Format<br>*.PEM - a Base64 encoded DER certificate<br>*.CER or *.CRT - Base64-encoded or DER-encoded binary X.509 Certificate<br>*.CRL - Certificate Revocation List<br>*.CSR - Certificate Signing Request<br>*.DER - DER-encoded binary X.509 Certificate<br>*.P7B or *.P7R or *.SPC - Cryptographic Message Syntax Standard<br>.Key – key files",
    "tags":[
        {
            "cloud":"git",
            "compliance":[
                "Best Practice"
            ],
            "service":[
                "common"
            ]
        }
    ],
    "resourceTypes":[
        "sensitive_extension"
    ],
    "status":"enable"
}]