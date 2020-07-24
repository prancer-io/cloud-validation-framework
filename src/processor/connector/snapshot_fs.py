"""
   Filesystem snapshot specific functionality using the base methods.
"""
import json
from processor.helper.file.file_utils import exists_file
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, json_from_file,\
    TEST, MASTERTEST, SNAPSHOT, MASTERSNAPSHOT, make_snapshots_dir,\
    store_snapshot, get_field_value_with_default, get_json_files, get_container_snapshot_json_files
from processor.helper.config.config_utils import config_value, framework_dir, get_test_json_dir
from processor.connector.snapshot_base import Snapshot
from processor.connector.snapshot_exception import SnapshotsException

logger = getlogger()


class FSSnapshot(Snapshot):
    """
    Filesystem snapshot utilities.
    """
    def __init__(self, container, snapshot_refactored_fns, singleTest=None):
        """ Default isDb is false, singletest shall be set to the test that needs to be run."""
        super().__init__(container, snapshot_refactored_fns)
        self.singleTest = singleTest
        reporting_path = config_value('REPORTING', 'reportOutputFolder')
        self.container_dir = '%s/%s/%s' % (framework_dir(), reporting_path, container)

    def get_structure_data(self, snapshot_object):
        """ Get the structure from the filesystem."""
        structure_data = {}
        json_test_dir = get_test_json_dir()
        snapshot_source = get_field_value(snapshot_object, "source")
        file_name = '%s.json' % snapshot_source if snapshot_source and not \
            snapshot_source.endswith('.json') else snapshot_source
        custom_source = '%s/../%s' % (json_test_dir, file_name)
        logger.info('%s structure file is %s', Snapshot.LOGPREFIX, custom_source)
        if exists_file(custom_source):
            structure_data = json_from_file(custom_source)
        return structure_data

    def get_used_snapshots_in_tests(self):
        """ Iterate through all snapshot and mastersnapshot and list the used snapshots in tests or mastertest."""
        snapshots = []
        logger.info("%s Fetching files for %s from container dir: %s", Snapshot.LOGPREFIX, self.container,
                    self.container_dir)
        for testType, snapshotType, replace in (
                (TEST, SNAPSHOT, False),
                (MASTERTEST, MASTERSNAPSHOT, True)):
            test_files = get_json_files(self.container_dir, testType)
            logger.info('%s fetched %s number of files from %s container: %s', Snapshot.LOGPREFIX, snapshotType,
                        self.container, len(test_files))
            snapshots.extend(self.process_files(test_files, snapshotType, replace))
        return list(set(snapshots))


    def process_files(self, test_files, doctype, replace=False):
        """ Process Test or masterTest json files."""
        snapshots = []
        for test_file in test_files:
            test_json_data = json_from_file(test_file)
            if test_json_data:
                snapshot = test_json_data[doctype] if doctype in test_json_data else ''
                if snapshot:
                    file_name = snapshot if snapshot.endswith('.json') else '%s.json' % snapshot
                    if replace:
                        file_name = file_name.replace('.json', '_gen.json')
                    if self.singleTest:
                        testsets = get_field_value_with_default(test_json_data, 'testSet', [])
                        for testset in testsets:
                            for testcase in testset['cases']:
                                if ('testId' in testcase and testcase['testId'] == self.singleTest) or \
                                        ('masterTestId' in testcase and testcase['masterTestId'] == self.singleTest):
                                    if file_name not in snapshots:
                                        snapshots.append(file_name)
                    else:
                        snapshots.append(file_name)
        return snapshots

    def store_data_node(self, data):
        """Store the data in the filesystem"""
        # Make a snapshots directory if DB is NONW
        snapshot_dir = make_snapshots_dir(self.container)
        if snapshot_dir:
            store_snapshot(snapshot_dir, data)

    def get_snapshots(self):
        """
        Get the snapshot files from the container with storage system as filesystem.
        The path for looking into the container is configured in the config.ini, for the
        default location configuration is $SOLUTIONDIR/relam/validation/<container>
        """
        snapshots_status = {}
        snapshot_dir, snapshot_files = get_container_snapshot_json_files(self.container)
        if not snapshot_files:
            logger.error("%s No Snapshot for this container: %s, in %s, add and run again!...", Snapshot.LOGPREFIX, self.container, snapshot_dir)
            raise SnapshotsException("No snapshots for this container: %s, add and run again!..." % self.container)
        used_snapshots = self.get_used_snapshots_in_tests()
        populated = []
        for snapshot_file in snapshot_files:
            parts = snapshot_file.rsplit('/', 1)
            if parts[-1] in used_snapshots and parts[-1] not in populated:
                # Take the snapshot and populate whether it was successful or not.
                # Then pass it back to the validation tests, so that tests for those
                # snapshots that have been susccessfully fetched shall be executed.
                file_name = '%s.json' % snapshot_file if snapshot_file and not snapshot_file.endswith('.json') else snapshot_file
                snapshot_json_data = json_from_file(file_name)
                if not snapshot_json_data:
                    logger.info("%s snapshot file %s looks to be empty, next!...",  Snapshot.LOGPREFIX, snapshot_file)
                    continue

                pull_response, git_connector_json = self.check_and_fetch_remote_snapshots(snapshot_json_data)
                if git_connector_json and not pull_response:
                    logger.info('%s Fetching remote snapshots failed.', Snapshot.LOGPREFIX)
                    break

                logger.debug(json.dumps(snapshot_json_data, indent=2))
                snapshot_data = self.populate_snapshots(snapshot_json_data)
                populated.append(parts[-1])
                name = parts[-1].replace('.json', '') if parts[-1].endswith('.json') else parts[-1]
                snapshots_status[name] = snapshot_data
        return snapshots_status
