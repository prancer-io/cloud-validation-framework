from processor.logging.log_handler import getlogger
logger = getlogger()

def sensitive_extensions(generated_snapshot, kwargs={}):
    paths = kwargs.get("paths", [])
    sensitive_extension_list = [
        ".pfx", ".p12", ".cer", ".crt", ".crl", ".csr", ".der", ".p7b", ".p7r", ".spc", ".pem"
    ]
    output = {}
    for path in paths:
        extension = "."+path.split(".")[-1]
        if sensitive_extension_list:
            if extension in sensitive_extension_list:
                output["issue"] = True
                output["skipped"] = False
                output["sensitive_extensions_err"] = "Sensitive files should not be checked into the git repo"
        else:
            output["issue"] = False
            output["skipped"] = False
    
    if not paths:
        output["issue"] = False
        output["skipped"] = False

    return output
