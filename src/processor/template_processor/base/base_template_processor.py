import time
import os
import hashlib
import pymongo
import hcl
from yaml.loader import FullLoader
from processor.helper.config.config_utils import config_value
from processor.helper.config.rundata_utils import get_dbtests
from processor.logging.log_handler import getlogger
from processor.database.database import insert_one_document, COLLECTION, DATABASE, DBNAME, \
    get_collection_size, create_indexes
from processor.helper.json.json_utils import get_field_value, store_snapshot, make_snapshots_dir
from processor.helper.yaml.yaml_utils import is_multiple_yaml_file,multiple_yaml_from_file,save_yaml_to_file,\
    is_multiple_yaml_convertion,is_helm_chart_convertion,MultipleConvertionKey,HelmChartConvertionKey\
    
from processor.templates.helm.helm_parser import HelmTemplateParser
from processor.helper.file.file_utils import exists_file, exists_dir

logger = getlogger()

class TemplateProcessor:
    """
    Base Template Processor for process template 
    parameters:
        node : node structure from snapshot JSON
        container: name of container on which the testcase is running
        dbname: collection name in which the data will store
        snapshot_source: name of the connector file
        snapshot_data: stores the snapshot results, require for run the test
        repopath: path to the temporary directory where the repository files are available
        processed_template: require to update this field with the processed template json
        paths: list of paths from the node structure json
        dir_path: path to the directory where the repository files are available, if `folderPath` is present in node.
                  otherwise it will same as `repopath`
        snapshot: snapshot structure
    """

    def __init__(self, node, **kwargs):
        self.node = node
        self.container = kwargs.get("container")
        self.dbname = kwargs.get("dbname")
        self.snapshot_source = kwargs.get("snapshot_source")
        self.connector_data = kwargs.get("connector_data")
        self.snapshot_data = kwargs.get("snapshot_data")
        self.repopath = kwargs.get("repopath")
        self.snapshot = kwargs.get("snapshot")
        self.processed_template = {}
        self.exclude_directories = []
        self.paths = []
        self.dir_path = ""
        self.template_files = []
        self.parameter_files = []

    def create_database_record(self):
        """
        returns a generated snapshot object from processed template for store it in database or file system
        """
        collection = self.node['collection'] if 'collection' in self.node else COLLECTION
        parts = self.snapshot_source.split('.')

        ref = ""
        if "branchName" in self.connector_data:
            ref = self.connector_data["branchName"]
        elif "folderPath" in self.connector_data:
            ref = self.connector_data["folderPath"]

        db_record = {
            "structure": self.connector_data["type"],
            "error": self.processed_template['error'] if 'error' in self.processed_template else None,
            "reference": ref,
            "source": parts[0],
            "paths": self.node["paths"],
            "timestamp": int(time.time() * 1000),
            "queryuser": self.connector_data['username'] if 'username' in self.connector_data else None,
            "checksum": hashlib.md5("{}".encode('utf-8')).hexdigest(),
            "node": self.node,
            "snapshotId": self.node['snapshotId'],
            "collection": collection.replace('.', '').lower(),
            "json": self.processed_template
        }
        return db_record
    
    def store_data_record(self):
        """
        creates the indexes on collection and stores the data record in database or creates
        the generated snapshot at file system
        """
        data_record = self.create_database_record()
        if get_dbtests():
            if get_collection_size(data_record['collection']) == 0:
                #Creating indexes for collection
                create_indexes(
                    data_record['collection'], 
                    config_value(DATABASE, DBNAME), 
                    [
                        ('snapshotId', pymongo.ASCENDING),
                        ('timestamp', pymongo.DESCENDING)
                    ]
                )

                create_indexes(
                    data_record['collection'], 
                    config_value(DATABASE, DBNAME), 
                    [
                        ('_id', pymongo.DESCENDING),
                        ('timestamp', pymongo.DESCENDING),
                        ('snapshotId', pymongo.ASCENDING)
                    ]
                )
            insert_one_document(data_record, data_record['collection'], self.dbname, check_keys=False)
        else:
            snapshot_dir = make_snapshots_dir(self.container)
            if snapshot_dir:
                store_snapshot(snapshot_dir, data_record)
            
        if 'masterSnapshotId' in self.node:
            self.snapshot_data[self.node['snapshotId']] = self.node['masterSnapshotId']
        else:
            self.snapshot_data[self.node['snapshotId']] = False if ('error' in data_record and data_record['error']) else True
        
        self.node['status'] = 'active'

    def process_template(self, paths):
        """
        process the files stored at specified paths and returns the processed template. 
        It should be override by child class for process the template files.
        """
        return {}
    
    def is_template_file(self, file_path):
        """
        checks that file located at given path is template file or not and return boolean value.
        It should be override by child class.
        """
        return False
    
    def is_parameter_file(self, file_path):
        """
        check that file located at given path is parameter file or not and return boolean value. 
        It should be override by child class.
        """
        return False
    
    def is_helm_chart_dir(self,file_path):
        """
        """
        file_type = file_path.split(".")[-1]
        file_name = file_path.split("/")[-1].split(".")[0]
        if file_type == "yaml" and file_name == "Chart" :
            helm_template = HelmTemplateParser(file_path)
            return helm_template.validate(file_path)
        return False

    def process_helm_chart(self,dir_path):
        helm_source_dir_name = dir_path.rpartition("/")[-1]
        helm_path = config_value('HELM','helmexe')
        result = os.system('%s template %s > %s/%s_prancer_helm_template.yaml' % (helm_path, dir_path,dir_path,helm_source_dir_name))
        paths = self.break_multiple_yaml_file('%s/%s_prancer_helm_template.yaml' % (dir_path,helm_source_dir_name))
        # os.remove('%s/Chart.yaml' % dir_path)
        return paths
        
        # helm_template = HelmTemplateParser()   
    def break_multiple_yaml_file(self,new_file_path):
        mutli_yaml = multiple_yaml_from_file(new_file_path,loader=FullLoader)
        paths=[]
        for index,single_object in enumerate(mutli_yaml) :
            new_file = '%s_multiple_yaml_%d.yaml' % (new_file_path.split(".")[0],index)
            save_yaml_to_file(single_object,new_file)
            if HelmChartConvertionKey in new_file_path :
                splited_path = new_file.rsplit("/",2)
                paths.append("/".join([splited_path[-2],splited_path[-1]]))
            else :
                paths.append(new_file.split("/",3)[-1])
        os.remove(new_file_path)
        return paths

    def populate_template_snapshot(self):
        """
        process the snapshot and returns the updated `snapshot_data` which is require for run the test
        """
        self.dir_path = get_field_value(self.connector_data, 'folderPath')
        if not self.dir_path:
            self.dir_path = self.repopath 

        self.paths = get_field_value(self.node, 'paths')
        if not self.paths or not isinstance(self.paths, list):
            self.node['status'] = 'inactive'
            logger.error("Invalid json : `paths` field is missing in node or it is not a list")
            return self.snapshot_data
        
        if is_multiple_yaml_convertion(self.paths[0]):
            multiple_source = '%s/%s.yaml' % (self.dir_path,(self.paths[0]).split(MultipleConvertionKey)[0])
            if exists_file(multiple_source):
                self.break_multiple_yaml_file(multiple_source)

        if is_helm_chart_convertion(self.paths[0]):
            helm_dir = '%s/%s' % (self.dir_path,self.paths[0].rpartition("/")[0]) 
            if not exists_file('%s/%s' % (helm_dir,self.paths[0].rpartition("/")[-1])):
                self.process_helm_chart(helm_dir)

        self.processed_template = self.process_template(self.paths)
        if self.processed_template:
            self.store_data_record()
            self.node['status'] = 'active'
        else:
            self.node['status'] = 'inactive'
        return self.snapshot_data
    
    def create_node_record(self, generated_template_file_list, count):
        """
        It is used in crawler. It creates a list of node objects for each generated snapshots.
        """
        nodes = []
        collection = get_field_value(self.node, 'collection')
        test_user = get_field_value(self.snapshot, 'testUser')
        source = get_field_value(self.snapshot, 'source')
        master_snapshot_id = get_field_value(self.node, 'masterSnapshotId')
        
        for template_node in generated_template_file_list:
            count = count + 1
            node_dict = {
                "snapshotId": '%s%s' % (master_snapshot_id, str(count)),
                "type": self.node["type"],
                "collection": collection,
                "paths": template_node["paths"],
                "status": template_node['status'],
                "validate": template_node['validate']
            }
            nodes.append(node_dict)
        return nodes, count
    
    def generate_template_and_parameter_file_list(self, file_path, template_file, parameter_file_list, generated_template_file_list):
        """
        process template and parameter files and returns the generated template file list
        """
        for parameter_file in parameter_file_list:
            paths = [
                template_file,
                parameter_file
            ]
            template_json = self.process_template(paths)
            if template_json:
                generated_template_file_list.append({
                    "paths" : [
                        ("%s/%s" % (file_path, template_file)).replace("//", "/"),
                        ("%s/%s" % (file_path, parameter_file)).replace("//", "/")
                    ],
                    "status" : "active",
                    "validate" : self.node['validate'] if 'validate' in self.node else True
                })
            else:
                generated_template_file_list.append({
                    "paths" : [
                        ("%s/%s" % (file_path, template_file)).replace("//", "/"),
                        ("%s/%s" % (file_path, parameter_file)).replace("//", "/")
                    ],
                    "status" : "inactive",
                    "validate" : self.node['validate'] if 'validate' in self.node else True
                })



    def populate_sub_directory_snapshot(self, file_path, base_dir_path, sub_dir_path, snapshot, dbname, node, snapshot_data, count):
        """
        Iterate the subdirectories for process each files inside the directory.
        """
        logger.info("Finding files in : %s" % sub_dir_path)
        dir_path = str('%s/%s' % (base_dir_path, sub_dir_path)).replace('//', '/')
        logger.info("dir_path   %s   : ",dir_path)

        if sub_dir_path in self.exclude_directories:
            logger.info("Excluded directory : %s", sub_dir_path)
            return count

        template_file_list = []
        parameter_file_list = []
        path_is_file,path_is_dir = False,False
        
        if exists_file(dir_path):
            path_is_file = True
        if exists_dir(dir_path):
            path_is_dir = True
       
        if any([path_is_dir,path_is_file]):
            if path_is_dir :
                list_of_file = os.listdir(dir_path)
                for entry in list_of_file:
                    new_dir_path = ('%s/%s' % (dir_path, entry)).replace('//', '/')
                    new_sub_directory_path = ('%s/%s' % (sub_dir_path, entry)).replace('//', '/')
                    if exists_dir(new_dir_path):
                        count = self.populate_sub_directory_snapshot(file_path, base_dir_path, new_sub_directory_path, snapshot, dbname, node, snapshot_data, count)
                    if self.is_helm_chart_dir(new_dir_path):
                        paths=self.process_helm_chart(dir_path)
                        template_file_list += paths
                    elif is_multiple_yaml_file(new_dir_path):
                        paths = self.break_multiple_yaml_file(new_dir_path)
                        template_file_list+=paths
                    elif exists_file(new_dir_path):
                        if self.is_template_file(new_dir_path):
                            template_file_list.append(new_sub_directory_path)
                        elif self.is_parameter_file(new_dir_path):
                            parameter_file_list.append(new_sub_directory_path)

            if path_is_file:
               template_file_list.append('%s' % (sub_dir_path).replace('//', '/'))

            logger.info("parameter_file_list   %s   : ", str(parameter_file_list))
            logger.info("template_file_list   %s   : ", str(template_file_list))
            generated_template_file_list = []
            if template_file_list:
                for template_file in template_file_list:
                    # template_file_path = str('%s/%s' % (base_dir_path, template_file)).replace('//', '/')
                    if parameter_file_list:
                        self.generate_template_and_parameter_file_list(file_path, template_file, parameter_file_list, generated_template_file_list)
                    else:
                        paths = [
                            template_file
                        ]
                        template_json = self.process_template(paths)
                        if template_json:
                            generated_template_file_list.append({
                                "paths" : [
                                    ("%s/%s" % (file_path, template_file)).replace("//", "/")
                                ],
                                "status" : "active",
                                "validate" : node['validate'] if 'validate' in node else True
                            })
                        else:
                            generated_template_file_list.append({
                                "paths" : [
                                    ("%s/%s" % (file_path, template_file)).replace("//", "/")
                                ],
                                "status" : "inactive",
                                "validate" : node['validate'] if 'validate' in node else True
                            })
                    
                nodes, count = self.create_node_record(generated_template_file_list, count)
                if self.node['masterSnapshotId'] not in self.snapshot_data or not isinstance(self.snapshot_data[self.node['masterSnapshotId']], list):
                    self.snapshot_data[self.node['masterSnapshotId']] = []
                self.snapshot_data[self.node['masterSnapshotId']] = self.snapshot_data[self.node['masterSnapshotId']] + nodes
        return count

    def populate_all_template_snapshot(self):
        """
        crawler function for populate all the files located at given paths and generate returns the updated `snapshot_data`
        """
        root_dir_path = get_field_value(self.connector_data, 'folderPath')
        if not root_dir_path:
            root_dir_path = self.repopath 

        self.paths = get_field_value(self.node, 'paths')

        if self.paths and isinstance(self.paths, list):
            count = 0
            for path in self.paths:
                self.dir_path = str('%s/%s' % (root_dir_path, path)).replace('//', '/')
                if exists_dir(self.dir_path):
                    path = path.rstrip("/")
                    count = self.populate_sub_directory_snapshot(path, self.dir_path, "", self.snapshot, self.dbname, self.node, self.snapshot_data, count)
                    # list_of_file = os.listdir(self.dir_path)
                    # for entry in list_of_file:
                    #     count = self.populate_sub_directory_snapshot(path, self.dir_path, entry, self.snapshot, self.dbname, self.node, self.snapshot_data, count)
                else:
                    logger.error("Invalid path : directory does not exist : " + self.dir_path)
        else:
            logger.error("\t\tERROR: Invalid json : `paths` is not a list or is not exist in master snapshot")    
        
        return self.snapshot_data
