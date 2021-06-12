
from processor.connector.git_connector.git_processor import git_clone_dir
from processor.logging.log_handler import getlogger

logger = getlogger()

class ModuleParser:
    
    def __init__(self, source, template_file_path, **kwargs):
        self.source = source
        self.template_file_path = template_file_path
        self.connector_data = kwargs.get("connector_data")
        self.module_file_path = None
    
    def process_source(self):
        if self.source.startswith(self.template_file_path) or self.source.startswith("./") or \
            self.source.startswith("../") or self.source.startswith('/'):
            return self.process_local_path()
        elif self.source.startswith('git::'):
            return self.process_git()
        elif 'github.com' in self.source:
            return self.process_github()

    def process_local_path(self):
        self.module_file_path = ("%s/%s" % (self.template_file_path, self.source)).replace("//","/")
        return self.module_file_path
    
    def process_git(self):
        self.source = self.source.replace('git::', '')
        if self.source.startswith('ssh:'):
            return self.module_file_path
        
        internal_dir = None
        if ".git//" in self.source:
            splited_url = self.source.split(".git//")
            git_url, internal_dir = splited_url[0], splited_url[1]
            self.source = git_url + ".git"
        
        repopath, _ = git_clone_dir(self.connector_data, giturl=self.source, clone_specific_branch=False)
        if not repopath:
            return self.module_file_path
        
        if internal_dir:
            repopath = ("%s/%s" % (repopath, internal_dir)).replace("//","/")
        self.module_file_path = repopath
        return self.module_file_path

    def process_github(self):
        internal_dir = None
        if ".git//" in self.source:
            splited_url = self.source.split(".git//")
            git_url, internal_dir = splited_url[0], splited_url[1]
            self.source = git_url + ".git"
        
        if self.source.startswith('git'):
            repo_path = self.source.replace(':', '/').split("github.com")
        else:
            repo_path = self.source.split("github.com")
        
        self.source = "https://github.com" + repo_path[-1]
        
        repopath, _ = git_clone_dir(self.connector_data, giturl=self.source, clone_specific_branch=False)
        if internal_dir:
            repopath = ("%s/%s" % (repopath, internal_dir)).replace("//","/")
        self.module_file_path = repopath
        return self.module_file_path