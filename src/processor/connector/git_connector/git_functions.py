from git import exc
from datetime import datetime
from git import Repo
import time
import re
import tempfile
import requests
import json

class GithubFunctions:

    def __init__(self):
        self.base_url = "https://api.github.com/"
        self.user = None
        self.repo = None
        self.access_token = None
    
    def set_access_token(self, access_token):
        """ get headers """
        self.access_token = access_token

    def get_headers(self):
        """ get headers """
        return { 
            "Accept" : "application/vnd.github.v3+json",
            "Authorization" : "Token %s" % self.access_token
        }

    def populate_user(self):
        """ get user object from access token """
        api_url = self.base_url + "user"
        response = requests.get(api_url, headers=self.get_headers())
        if response.status_code == 200:
            self.user = response.json()
        return self.user
    
    def get_user(self):
        return self.user

    def create_pull_request(self, source_repo, title, from_branch, to_branch):
        """ create pull request """

        match_values = re.search(r'(?<=\.com\/)(.*)(?=.git)', source_repo, re.I)
        if match_values:
            api_url = self.base_url + "repos/%s/pulls" % match_values.group(0)
            data = { "head": to_branch, "base": from_branch, "title" : title }

            response = requests.post(api_url, data=json.dumps(data), headers=self.get_headers())
            if response.status_code in [200, 201] :
                response_data = response.json()
                return response_data.get("html_url")
        return None
    
    def clone_repo(self, source_repo, clone_path, branch_name=None):
        """ clone repository at provided path """
        
        if source_repo.startswith('git'):
            repo_path = source_repo.replace(':', '/').split("github.com")
        else:
            repo_path = source_repo.split("github.com")
        
        if self.user and self.access_token and self.user.get("login"):
            source_repo = "https://" + self.user.get("login") + ":" + self.access_token +"@github.com" + repo_path[-1]
        else:
            source_repo = "https://github.com" + repo_path[-1]

        kwargs = {
            "depth" : 1
        }
        if branch_name:
            kwargs["branch"] = branch_name
            
        self.repo = Repo.clone_from(
            source_repo,
            clone_path,
            **kwargs
        )
        return self.repo
    
    def checkout_branch(self, branch_name):
        """ checkout branch """
        try:
            self.repo.git.checkout('-b', branch_name)
            return True
        except:
            return False

    def commit_changes(self, commit_message=""):
        """ commit the changes """
        try:
            self.repo.git.add(".")
            self.repo.index.commit(commit_message)
        except:
            return False

    def push_changes(self, branch_name):
        """ Push the code to git """
        try:
            self.repo.create_head(branch_name)
            origin = self.repo.remote()
            origin.push(branch_name)
            return True
        except:
            return False


if __name__ == '__main__':
    import sys
    import tempfile
    if len(sys.argv) > 2:
        tk = sys.argv[1]
        repoUrl = sys.argv[2]
        clonedir = tempfile.mkdtemp()
        gh = GithubFunctions()
        gh.set_access_token(tk)
        usr = gh.populate_user()
        rpo = gh.clone_repo(repoUrl, clonedir, 'master')
        if rpo:
            print('Successfully cloned in %s dir' % clonedir)
        else:
            print('Failed to  clone %s ' % repoUrl)
    else:
        print('Provide access token and repository https URL')
            
    
