""" Driver file to convert terraform to json files """


if __name__ == "__main__":
    import sys
    from processor.helper.utils.cli_terraform_to_json import terraform_to_json_main
    sys.exit(terraform_to_json_main())
