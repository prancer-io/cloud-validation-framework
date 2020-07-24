"""
   Base snapshot for filesystem, db etc.
"""
import hcl

from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, json_from_file
from processor.connector.populate_json import pull_json_data
from processor.helper.yaml.yaml_utils import yaml_from_file


logger = getlogger()


class Snapshot:
    """ Base class for snapshot processing"""

    LOGPREFIX = 'Snapshots:'
    # snapshot_fns = {
    #     'azure1': populate_snapshot_azure,
    #     'azure': populate_azure_snapshot,
    #     'filesystem': populate_custom_snapshot
    # }

    def __init__(self, container, snapshot_refactored_fns):
        """ Base class, where all attributes are false."""
        self.container = container
        self.snapshot_fns = snapshot_refactored_fns
        self.appObject = {}
        self.singleTest = None
        self.isDb = False

    def store_value(self, key, value):
        """ Store key value used down the p[rocessing stream."""
        if key and value:
            self.appObject[key] = value

    def get_value(self, key):
        """ Use the app storage and will be garbage collected after the completion of the snapshot fetch process."""
        if key and key in self.appObject:
            return self.appObject.get(key)
        return None

    def get_snapshots(self):
        """ Iterator based implementation"""
        return []

    def get_snapshot_nodes(self, snapshot):
        """ Iterate over the nodes of the snapshot object"""
        snapshot_nodes = get_field_value(snapshot, 'nodes')
        return snapshot_nodes if snapshot_nodes else []

    def validate_snapshot_ids_in_nodes(self, snapshot):
        """ The snapshotsIds should be strings and also quoted."""
        snapshot_data = {}
        valid_snapshotids = True
        for node in self.get_snapshot_nodes(snapshot):
            if 'snapshotId' in node and node['snapshotId']:
                snapshot_data[node['snapshotId']] = False
                if not isinstance(node['snapshotId'], str):
                    valid_snapshotids = False
            elif 'masterSnapshotId' in node and node['masterSnapshotId']:
                snapshot_data[node['masterSnapshotId']] = False
                if not isinstance(node['masterSnapshotId'], str):
                    valid_snapshotids = False
            else:
                logger.error(
                    'All snapshot nodes should contain snapshotId or masterSnapshotId attribute with a string value')
                valid_snapshotids = False
                break
        if not valid_snapshotids:
            logger.error('All snapshot Ids should be strings, even numerals should be quoted')
        return snapshot_data, valid_snapshotids

    def check_and_fetch_remote_snapshots(self, json_data):
        """Could be snapshot that snapshots are fetched from remote repository."""
        git_connector_json = False
        pull_response = False
        if "connector" in json_data and "remoteFile" in json_data and \
                json_data["connector"] and json_data["remoteFile"]:
            git_connector_json = True
            _, pull_response = pull_json_data(json_data)
        return pull_response, git_connector_json

    def get_structure_data(self, snapshot_object):
        """ Return a empty dict in base class."""
        structure_data = {}
        return structure_data

    def store_data_node(self, data):
        """ Store the data record as per the data system"""
        return False

    def populate_snapshots(self, snapshot_json_data):
        """
        Every snapshot should have collection of nodes which are to be populated.
        Each node in the nodes list of the snapshot shall have a unique id in this
        container so as not to clash with other node of a snapshots.
        """
        snapshot_data = {}
        snapshots = get_field_value(snapshot_json_data, 'snapshots')
        if not snapshots:
            logger.error("Json Snapshot does not contain snapshots, next!...")
            return snapshot_data
        for snapshot in snapshots:
            connector_data = self.get_structure_data(snapshot)
            snapshot_type = get_field_value(connector_data, "type")
            if snapshot_type and snapshot_type in self.snapshot_fns:
                if 'nodes' not in snapshot or not snapshot['nodes']:
                    logger.error("No nodes in snapshot to be backed up!...")
                    return snapshot_data
                if snapshot_type == 'azure' or snapshot_type == 'filesystem':
                    current_data = self.snapshot_fns[snapshot_type](snapshot, self.container)
                else:
                    current_data = self.snapshot_fns[snapshot_type](snapshot, self)
                logger.info('Snapshot: %s', current_data)
                snapshot_data.update(current_data)
        return snapshot_data

    @classmethod
    def convert_to_json(cls, file_path, file_type):
        json_data = {}
        if file_type == 'json':
            json_data = json_from_file(file_path, escape_chars=['$'])
        elif file_type == 'terraform':
            with open(file_path, 'r') as fp:
                json_data = hcl.load(fp)
        elif file_type == 'yaml' or file_type == 'yml':
            json_data = yaml_from_file(file_path)
        else:
            logger.error("Fileconversion error type:%s and file: %s", file_type, file_path)
        return json_data
