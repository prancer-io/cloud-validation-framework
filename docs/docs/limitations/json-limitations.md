Because the **Git** connector is loading whole files at once as resources, it means you cannot use parts of the **JSON** file as a resource. This might be an issue if your **JSON** file is pretty complex. Fear not, there are workarounds!

Another limitation is that some **JSON** files feature keys with `$` signs in them. This is considered a special notation for reserved keywords in **JSON** and this is forbidden in **MongoDB**.

# Reserved keywords in MongoDB

If you import a file with a key like `$schema` in **Prancer**, it will automatically be escaped like this:

    \$schema

So when using a test in **Prancer** for such keys (You probably shouldn't be testing these fields) then they should use:

    "\\\$schema"

as a reference to properly escape the value.

# Use an external tool to chunk the file

By using a tool like **jq**, you can extract portions of your **JSON** file into smaller files. If you integrate this into your build system, you can easily generate chunks of your file and then use those temporary files as snapshots.

Take the following **JSON** file into account and note that this file is almost 3000 lines long normally:

    {
        "AD": {
            "name": "Andorra",
            "native": "Andorra",
            "phone": "376",
            "continent": "EU",
            "capital": "Andorra la Vella",
            "currency": "EUR",
            "languages": [
                "ca"
            ]
        },
        "AE": {
            "name": "United Arab Emirates",
            "native": "دولة الإمارات العربية المتحدة",
            "phone": "971",
            "continent": "AS",
            "capital": "Abu Dhabi",
            "currency": "AED",
            "languages": [
                "ar"
            ]
        },
        "AF": {
            "name": "Afghanistan",
            "native": "افغانستان",
            "phone": "93",
            "continent": "AS",
            "capital": "Kabul",
            "currency": "AFN",
            "languages": [
                "ps",
                "uz",
                "tk"
            ]
        },
        "AG": {
            "name": "Antigua and Barbuda",
            "native": "Antigua and Barbuda",
            "phone": "1268",
            "continent": "NA",
            "capital": "Saint John's",
            "currency": "XCD",
            "languages": [
                "en"
            ]
        },
        "AI": {
            "name": "Anguilla",
            "native": "Anguilla",
            "phone": "1264",
            "continent": "NA",
            "capital": "The Valley",
            "currency": "XCD",
            "languages": [
                "en"
            ]
        }
    }

Doing tests over this file isn't too complex because there aren't many layers of objects but all tests would still look like this:

    {countries}.AE.languages[] == ['ca']

In a much more complex file, the repetition of `{countries}.AE` would be a real pain. Therefore, you might need a way to simplify your huge file. To do this, you can use the following workaround.

A quick and dirty example would be:

    cat "countries.json" | jq '.AE.languages' > "output-ae.json"
    cat "countries.json" | jq '.AI.languages' > "output-ai.json"

Then, you should just commit those files to **Git** and use them in your **Prancer** test suite just like a file that would normally exist.