Before digging deeper into rule systax, let's look at how you can inspect the database server to view the data and craft proper rules.

# Connecting to MongoDB

First, connect to your **MongoDB** database server using the tool of your choice. We'll assume the use of the default **mongo** shell client but you can use any client you want.

Open a terminal and start the `mongo` shell client, then select the default `validator` database:

    mongo
    use validator

Refer to the [MongoDB Shell client](https://docs.mongodb.com/manual/mongo/) documentation page for more information on how to use the tool.

# List the different collections

**MongoDB** stores data in collections, hence the term **collection-name** that you have seen in previous sections regarding **snapshots**. To list all collections in the database you can use:

    show collections

This will list all the collections in the database.

# Showing data in a collection

To show data from a collection you can run a simple statement:

    db.<collection-name>.find().pretty()

Replace the `<collection-name>` with one of the collection names you got from the previous listing.

This will output a lot of information. (or maybe nothing at all if you haven't run any tests yet)

When you look at the data from the collection, you should see a rather complete and complex **JSON** document that would look something like this:

    {
        "_id" : ObjectId("5cb483ef7554c1573a4d3402"),
        "checksum" : "cac2c001358b0c67247bb34bc21235bf",
        "collection" : "security_groups",
        "json" : {
            "ResponseMetadata" : {
                "HTTPHeaders" : {
                    "content-length" : "1042",
                    "content-type" : "text/xml;charset=UTF-8",
                    "date" : "Mon, 15 Apr 2019 13:15:27 GMT",
                    "server" : "AmazonEC2"
                },
                "HTTPStatusCode" : 200,
                "RequestId" : "e0806089-4215-479c-99b3-87f5a52bb273",
                "RetryAttempts" : 0
            },
            "SecurityGroups" : [
                {
                    "Description" : "prancer-tutorial-sg",
                    "GroupName" : "prancer-tutorial-sg",
                    "IpPermissions" : [ ],
                    "OwnerId" : "667095293603",
                    "GroupId" : "sg-0125a7610cd1dd391",
                    "IpPermissionsEgress" : [
                        {
                            "IpProtocol" : "-1",
                            "IpRanges" : [
                                {
                                    "CidrIp" : "0.0.0.0/0"
                                }
                            ],
                            "Ipv6Ranges" : [ ],
                            "PrefixListIds" : [ ],
                            "UserIdGroupPairs" : [ ]
                        }
                    ],
                    "VpcId" : "vpc-050b8b70e3593efd2"
                }
            ]
        },
        "node" : {
            "collection" : "security_groups",
            "id" : {
                "GroupNames" : [
                    "prancer-tutorial-sg"
                ]
            },
            "snapshotId" : 2,
            "type" : "security_groups"
        },
        "path" : "",
        "queryuser" : "",
        "reference" : "",
        "snapshotId" : 2,
        "source" : "awsStructure",
        "structure" : "aws",
        "timestamp" : NumberLong("1555334127715")
    }

This document is what **Prancer** stores on each validation run for each snapshot.

In each document, you can find a property called `json`. The content of this property is what is made available to you when you refer to a snapshot from a rule. For example:

    {2}.SecurityGroups[0].Description = 'Some description'

Is the equivalent of:

    {"ResponseMetadata":{"HTTPHeaders":{"content-length":"1042","content-type":"text/xml;charset=UTF-8","date":"Mon, 15 Apr 2019 13:15:27 GMT","server":"AmazonEC2"},"HTTPStatusCode":200,"RequestId":"e0806089-4215-479c-99b3-87f5a52bb273","RetryAttempts":0},"SecurityGroups":[{"Description":"prancer-tutorial-sg","GroupName":"prancer-tutorial-sg","IpPermissions":[],"OwnerId":"667095293603","GroupId":"sg-0125a7610cd1dd391","IpPermissionsEgress":[{"IpProtocol":"-1","IpRanges":[{"CidrIp":"0.0.0.0/0"}],"Ipv6Ranges":[],"PrefixListIds":[],"UserIdGroupPairs":[]}],"VpcId":"vpc-050b8b70e3593efd2"}]}.SecurityGroups[0].Description = 'Some description'

or in a simpler form:

    {"Description":"prancer-tutorial-sg","GroupName":"prancer-tutorial-sg","IpPermissions":[],"OwnerId":"667095293603","GroupId":"sg-0125a7610cd1dd391","IpPermissionsEgress":[{"IpProtocol":"-1","IpRanges":[{"CidrIp":"0.0.0.0/0"}],"Ipv6Ranges":[],"PrefixListIds":[],"UserIdGroupPairs":[]}],"VpcId":"vpc-050b8b70e3593efd2"}.Description = 'Some description'

and in the simplest form possible:

    'prancer-tutorial-sg' = 'Some description'

Which would result in a `False` result and fail the test.

# Writing complex queries

Because your **MongoDB** database will get fat pretty fast, it is important to learn how to properly query it. We will not go into a lot of details here, you can consult the [Mongo Query Document](https://docs.mongodb.com/manual/tutorial/query-documents/) documentation page to know more.

Here are a few approaches to finding the proper data in your database.

To query for all snapshot data of a specific snapshot definition you could issue the next statement:

    db.security_groups.find({node:{snapshotId:2}).pretty()

If you want only the latest item you can use the `_id` field's automatic datation using:

    db.security_groups.find({node:{snapshotId:2}).sort({_id:1}).limit(1).pretty()

There are many different ways you can use the `mongo` shell to inspect your data. Keep in mind that the [Mongo Query Document](https://docs.mongodb.com/manual/tutorial/query-documents/) documentation page is your best friend in this case.