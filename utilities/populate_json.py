""" Driver file for populating json files to database """


if __name__ == "__main__":
    import sys
    from processor.helper.utils.cli_populate_json import populate_json_main
    sys.exit(populate_json_main())
