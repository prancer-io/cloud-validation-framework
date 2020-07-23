"""
   Filesystem snapshot specific functionality using the base methods.
"""
import pymongo
from processor.logging.log_handler import getlogger
from processor.helper.json.json_utils import get_field_value, collectiontypes, \
    STRUCTURE, TEST, MASTERTEST, SNAPSHOT, MASTERSNAPSHOT
from processor.helper.config.config_utils import config_value
from processor.database.database import insert_one_document, get_collection_size, create_indexes, \
     DATABASE, DBNAME, sort_field, get_documents, update_one_document
from processor.reporting.json_output import dump_output_results
from processor.connector.snapshot_base import Snapshot
from processor.connector.snapshot_exception import SnapshotsException


logger = getlogger()


class DBSnapshot(Snapshot):
    """
    Database snapshot utilities.
    """
    def __init__(self, container, snapshot_refactored_fns):
        """"DB is true, will be usefule to make checks."""
        super().__init__(container)
        self.dbname = config_value(DATABASE, DBNAME)
        self.qry = {'container': container}
        self.sort = [sort_field('timestamp', False)]
        self.isDb = True

    def collection(self, name=TEST):
        """ Get the collection name for the json object"""
        return config_value(DATABASE, collectiontypes[name])

    def get_structure_data(self, snapshot_object):
        """ Return the structure from the database"""
        structure_data = {}
        snapshot_source = get_field_value(snapshot_object, "source")
        snapshot_source = snapshot_source.replace('.json', '') if snapshot_source else ''
        qry = {'name': snapshot_source}
        structure_docs = get_documents(self.collection(STRUCTURE), dbname=self.dbname, sort=self.sort, query=qry, limit=1)
        logger.info('%s fetched %s number of documents: %s', Snapshot.LOGPREFIX, STRUCTURE, len(structure_docs))
        if structure_docs and len(structure_docs):
            structure_data = structure_docs[0]['json']
        return structure_data

    def get_used_snapshots_in_tests(self):
        """ Get the snapshots used in test and mastertest of the container."""
        snapshots = []
        logger.info("%s Fetching documents for %s", Snapshot.LOGPREFIX, self.container)
        for collection, snapshotType, suffix in (
                (TEST, SNAPSHOT, ''),
                (MASTERTEST, MASTERSNAPSHOT, '_gen')):
            docs = get_documents(self.collection(collection), dbname=self.dbname, sort=self.sort, query=self.qry)
            logger.info('%s fetched %s number of documents: %s', Snapshot.LOGPREFIX, collection, len(docs))
            snapshots.extend(self.process_docs(docs, snapshotType, suffix))
        return list(set(snapshots))

    def get_snapshots(self):
        """Populate the used snapshots in test and mastertest for this container."""
        snapshots_status = {}
        docs = get_documents(self.collection(SNAPSHOT), dbname=self.dbname, sort=self.sort, query=self.qry, _id=True)
        if docs and len(docs):
            logger.info('%s fetched %s number of documents: %s', Snapshot.LOGPREFIX, SNAPSHOT, len(docs))
            used_snapshots = self.get_used_snapshots_in_tests()
            if not used_snapshots:
                raise SnapshotsException("No snapshots for this container: %s, add and run again!..." % self.container)
            populated = []
            for doc in docs:
                if doc['json']:
                    snapshot = doc['name']
                    try:
                        pull_response, git_connector_json = self.check_and_fetch_remote_snapshots(doc['json'])
                        if git_connector_json and not pull_response:
                            logger.info('%s Fetching remote snapshots failed.', Snapshot.LOGPREFIX)
                            break

                        if snapshot in used_snapshots and snapshot not in populated:
                            # Take the snapshot and populate whether it was successful or not.
                            # Then pass it back to the validation tests, so that tests for those
                            # snapshots that have been susccessfully fetched shall be executed.
                            snapshot_file_data = self.populate_snapshots(doc['json'])

                            if not git_connector_json:
                                update_one_document(doc, self.collection(SNAPSHOT), self.dbname)

                            populated.append(snapshot)
                            snapshots_status[snapshot] = snapshot_file_data
                    except Exception as e:
                        dump_output_results([], self.container, "-", snapshot, False)
                        raise e
        if not snapshots_status:
            raise SnapshotsException("No snapshots for this container: %s, add and run again!..." % self.container)
        return snapshots_status

    def process_docs(self, docs, doctype, suffix=''):
        """ Process Test or masterTest documents"""
        snapshots = []
        if docs and len(docs):
            for doc in docs:
                if doc['json']:
                    snapshot = doc['json'][doctype] if doctype in doc['json'] else ''
                    if snapshot:
                        snapshots.append((snapshot.split('.')[0] if snapshot.endswith('.json') else snapshot) + suffix)
        return snapshots

    def store_data_node(self, data):
        """ Store to database"""
        if get_collection_size(data['collection']) == 0:
            # Creating indexes for collection
            create_indexes(
                data['collection'],
                config_value(DATABASE, DBNAME),
                [
                    ('snapshotId', pymongo.ASCENDING),
                    ('timestamp', pymongo.DESCENDING)
                ]
            )

            create_indexes(
                data['collection'],
                config_value(DATABASE, DBNAME),
                [
                    ('_id', pymongo.DESCENDING),
                    ('timestamp', pymongo.DESCENDING),
                    ('snapshotId', pymongo.ASCENDING)
                ]
            )
        insert_one_document(data, data['collection'], self.dbname, check_keys=False)
