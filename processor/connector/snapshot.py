"""
   Common file for running snapshot functions.
"""
import json
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    get_container_snapshot_json_files
from processor.connector.snapshot_azure import populate_azure_snapshot
from processor.connector.snapshot_custom import populate_custom_snapshot


logger = getlogger()
snapshot_fns = {
    'azure': populate_azure_snapshot,
    'custom': populate_custom_snapshot
}


def populate_snapshot(snapshot):
    snapshot_type = get_field_value(snapshot, 'type')
    if snapshot_type and snapshot_type in snapshot_fns:
        if 'nodes' not in snapshot or not snapshot['nodes']:
            logger.info("No nodes in snapshot to be backed up!...")
            return False
        return snapshot_fns[snapshot_type](snapshot)
    return False


def populate_snapshots_from_json(snapshot_json_data):
    snapshots = get_field_value(snapshot_json_data, 'snapshots')
    if not snapshots:
        logger.info("Json Snapshot does not contain snapshots, next!...")
        return False
    for snapshot in snapshots:
        populate_snapshot(snapshot)
    return True


def populate_snapshots_from_file(snapshot_file):
    """Load the file as json and populate from json file."""
    snapshot_json_data = json_from_file(snapshot_file)
    if not snapshot_json_data:
        logger.info("Snapshot file %s looks to be empty, next!...", snapshot_file)
        return False
    logger.debug(json.dumps(snapshot_json_data, indent=2))
    return populate_snapshots_from_json(snapshot_json_data)


def populate_container_snapshots(container):
    """ Get the snapshot files in the container"""
    snapshot_dir, snapshot_files = get_container_snapshot_json_files(container)
    if not snapshot_files:
        logger.info("No Snapshot files in %s, exiting!...", snapshot_dir)
        return False
    logger.info('\n'.join(snapshot_files))
    for snapshot_file in snapshot_files:
        populate_snapshots_from_file(snapshot_file)
    return True

