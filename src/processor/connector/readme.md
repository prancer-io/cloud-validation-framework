
1) Introduction:
Snapshot connector takes snapshot configuration as its input and fetches snapshots in the snapshot configuration. These snapshots are then put under test to evaluate test
expectations for a favorable outputs. The snapshots are fetched using connector configuration. The connector configuration is different for each provider viz. azure, aws, git,
google oracle, terraform etc. This implementation for each connector is responsible to fetch using the specifics of the connector mechanism provided.

2) Description:
  1) Steps to connector.
  2) Files to be implmeneted.
  3) Integrate into the system.

3) Details:

3A) Helpers from the framework:

1) fs_snapshot:
    
  Constructed by the framework for a container  and has all utility functionalities for filesystem operations.

  1) Get all list of snapshot files for a container( used_in_test = True) parameter will give used in a test
  2) Get all list of mastersnapshot files for a container( used_in_test = True) parameter will give used used in a mastertest
  3) Check a snapshot/mastersnapshot is valid and of the type(azure)
  4) Iterate all the snapshots in a in the 'snapshots' field of a configuration file.

2) db_snapshot:

  Constructed by the framework for a container  and all utility functions for DB operations.

  1) Get all list of snapshot documents for a container( used_in_test = True) parameter will give used in a test
  2) Get all list of mastersnapshot files for a container( used_in_test = True) parameter will give used used in a mastertest
  3) Check a snapshot/mastersnapshot is valid and of the type(azure)
  4) Iterate all the snapshots in the 'snapshots' field of a configuration file.

3) application cache:
  1) Store and retrieve any key-value pairs during the run. eg: Bearer token
  2) This object shall be destroyed and its content shall be destroyed post the populate_snapshot operation


3B) Snapshot implementation:

1) Snapshots could be stored in a filesystem as json files or db records in mongo database. In a db record there is metadata stored in the top level fields
   and the snapshot data is stored in 'json' field. The important fields are 'name' and 'container' of the snapshot. For a filesystem the container name is the
    directory and the snapshot name is the filename. 

   populate_snapshot_<name>(snapshot_object, <fs/db>_snapshot) eg: populate_snapshot_azure, populate_snapshot_custom

   Input:
    snapshot_object: The structure of snapshot as per prancer framework.
    <fs/db>_snapshot: This object shall be initialized for filesystem or container container operations.

   Flow:
    Get list of snapshot configurations
    Iterate thru each snapshot configuration
        Check valid and is of type being implemented(eg azure)
        Iterate through each snapshot configuration
           Specific logic for getting the connector and the user to be used from the connector.
           Crawl or fetch operation decision.
           Fetch individual node(s) using the connector and call store_data_node on fs_snapshot or db_snapshot to insert.
           Update successful or failure for snapshot fetching.

   Exception:
     Container does not exist (SnaphotsException)
     Container does not contain any snapshot/mastersnapshot files (SnaphotsException)
     Connector connection failure (SnaphotsException)
     Connector error viz. permission. (SnaphotsException)
     Snapshot invalid json( Mostly applicable when stored on filesystem) on mongo should be a valid json object
     Resource missing should not be an exception, it should be updated in snapshot as false, with validate as False
 
   Errors:
     Invalid snapshots like user, source or nodes missing or empty nodes.

   Logging:
     Info:
        All snapshot iterations
        All snapshot iteration from each snapshot object
        Individual snapshot fetch operation.
        Successful store to data layer(filesystem or database)
     Error/Critical:
        Any snapshot object missing. Action is to make the snapshot=False, and validate=False
     Debug:
        Data objects.Sensistive information to be masked using the application cache object.
        
   Output:
     Objects fetched with True or False for tests to be run.


   Others:
     Attributes like single test, check snapshot duplication fetch 
