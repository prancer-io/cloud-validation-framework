"""
Snapshot utils contains common functionality for all snapshots.
"""
import time
import hashlib
from processor.database.database import COLLECTION, get_documents
from processor.logging.log_handler import getlogger


logger = getlogger()


def validate_snapshot_nodes(snapshot_nodes):
    snapshot_data = {}
    valid_snapshotids = True
    if snapshot_nodes:
        for node in snapshot_nodes:
            if 'snapshotId' in node and  node['snapshotId']:
                snapshot_data[node['snapshotId']] = False
                if not isinstance(node['snapshotId'], str):
                    valid_snapshotids = False
            elif 'masterSnapshotId' in node and node['masterSnapshotId']:
                snapshot_data[node['masterSnapshotId']] = False
                if not isinstance(node['masterSnapshotId'], str):
                    valid_snapshotids = False
            else:
                logger.error('All snapshot nodes should contain snapshotId or masterSnapshotId attribute with a string value')
                valid_snapshotids = False
                break
            # snapshot_data[node['snapshotId']] = False
            # if not isinstance(node['snapshotId'], str):
            #     valid_snapshotids = False
    if not valid_snapshotids:
        logger.error('All snapshot Ids should be strings, even numerals should be quoted')
    return snapshot_data, valid_snapshotids


def get_data_record(ref_name, node, user, snapshot_source, connector_type):
    """ The data node record, common function across connectors."""
    collection = node['collection'] if 'collection' in node else COLLECTION
    parts = snapshot_source.split('.')
    return {
        "structure": connector_type,
        "reference": ref_name,
        "source": parts[0],
        "path": '',
        "timestamp": int(time.time() * 1000),
        "queryuser": user,
        "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
        "node": node,
        "snapshotId": node['snapshotId'] if 'snapshotId' in node else '',
        "mastersnapshot": False,
        "masterSnapshotId": node['masterSnapshotId'] if 'masterSnapshotId' in node else '',
        "collection": collection.replace('.', '').lower(),
        "json": {}  # Refactor when node is absent it should None, when empty object put it as {}
    }