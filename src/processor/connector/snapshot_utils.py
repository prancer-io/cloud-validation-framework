"""
Snapshot utils contains common functionality for all snapshots.
"""

from processor.logging.log_handler import getlogger
logger = getlogger()


def validate_snapshot_nodes(snapshot_nodes):
    snapshot_data = {}
    valid_snapshotids = True
    if snapshot_nodes:
        for node in snapshot_nodes:
            snapshot_data[node['snapshotId']] = False
            if not isinstance(node['snapshotId'], str):
                valid_snapshotids = False
    if not valid_snapshotids:
        logger.error('All snapshot Ids should be strings, even numerals should be quoted')
    return snapshot_data, valid_snapshotids