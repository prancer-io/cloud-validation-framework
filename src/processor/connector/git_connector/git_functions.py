from git import exc
from datetime import datetime
from git import Repo
import urllib.parse
import time
import re
import tempfile
import requests
import json

CLONE_REPOS = []
GITHUB_URL = "https://api.github.com/"

def set_clone_repo(git_cmd, repo, clone_dir):
    global CLONE_REPOS
    CLONE_REPOS.append({
        "git_command" : git_cmd,
        "repo" : repo,
        "clonedir" : clone_dir
    })

def check_clone_repos(git_cmd):
    global CLONE_REPOS
    for repo in CLONE_REPOS:
        if repo.get("git_command") == git_cmd:
            return repo.get("repo"), repo.get("clonedir")
    return None, None

class GithubFunctions:

    def __init__(self):
        self.base_url = GITHUB_URL
        self.user = None
        self.repo = None
        self.access_token = None
        self.is_bearer_token = False

    def set_base_url(self, base_url):
        """ set base url for enterprise github"""
        self.base_url = base_url
        self.check_is_bearer_token(base_url)

    def set_access_token(self, access_token):
        """ get headers """
        self.access_token = access_token

    def check_is_bearer_token(self, base_url):
        """ Is it a bearer token to pass as an additional header to clone """
        if base_url:
            giturl = urllib.parse.unquote(base_url)
            urlval = urllib.parse.urlparse(giturl)
            if urlval.netloc.endswith('azure.com'):
                self.is_bearer_token = True

    def get_headers(self):
        """ get headers """
        if self.is_bearer_token:
            return {
                "Accept" : "application/json"
            }
        else:
            return {
                "Accept" : "application/vnd.github.v3+json",
                "Authorization" : "Token %s" % self.access_token
            }

    def populate_user(self):
        """ get user object from access token """
        giturl = urllib.parse.unquote(self.base_url)
        urlval = urllib.parse.urlparse(giturl)
        if self.is_bearer_token:
            if urlval.netloc.endswith('azure.com'):
                vals = urlval.netloc.split('@')
                self.user = {'login': vals[0]}
        else:
            if urlval.netloc.endswith('github.com'):
                api_url = GITHUB_URL + "user"
            else:
                api_url = urlval.scheme + "://" + urlval.netloc + "/api/v3/user"
            # api_url = self.base_url + "user"
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
        cval = None
        giturl = urllib.parse.unquote(source_repo)
        urlval = urllib.parse.urlparse(giturl)
        if urlval.netloc.endswith('github.com'):
            if source_repo.startswith('git'):
                repo_path = source_repo.replace(':', '/').split("github.com")
            else:
                repo_path = source_repo.split("github.com")
        
            if self.user and self.access_token and self.user.get("login"):
                source_repo = "https://" + self.user.get("login") + ":" + self.access_token +"@github.com" + repo_path[-1]
            else:
                source_repo = "https://github.com" + repo_path[-1]
        elif urlval.netloc.endswith('azure.com'):
            # Dont change source repo.
            cval="http.extraHeader=Authorization: Bearer %s" % self.access_token
        else:
            if self.user and self.access_token and self.user.get("login"):
                source_repo = urlval.scheme + "://" + self.user.get("login") + ":" + self.access_token + "@" + urlval.netloc + urlval.path
            else:
                source_repo = urlval.scheme + "://" + urlval.netloc + urlval.path

        kwargs = {"depth": 1}

        if branch_name:
            kwargs["branch"] = branch_name

        if cval:
            self.repo = Repo.clone_from(
                source_repo,
                clone_path,
                env={'GIT_SSL_NO_VERIFY': '1'},
                c=cval,
                **kwargs
            )
        else:
            self.repo = Repo.clone_from(
                source_repo,
                clone_path,
                env={'GIT_SSL_NO_VERIFY': '1'},
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
    import os
    if len(sys.argv) > 2:
        tk = sys.argv[1]
        repoUrl = sys.argv[2]
        clonedir = tempfile.mkdtemp()
        gh = GithubFunctions()
        gh.set_access_token(tk)
        urlval = urllib.parse.urlparse(repoUrl)
        if urlval.netloc.endswith('github.com'):
            baseurl = 'https://api.github.com/'
        else:
            baseurl = urlval.scheme + "://" + urlval.netloc + "/api/v3/"
        gh.set_base_url(baseurl)
        gh.populate_user()
        rpo = gh.clone_repo(repoUrl, clonedir, 'master')
        if rpo:
            print('Successfully cloned in %s dir' % clonedir)
        else:
            print('Failed to  clone %s ' % repoUrl)
    else:
        tkn = os.environ.get('TOKEN', None)
        source_repo = os.environ.get('REPOURL', None)
        if tkn is None or source_repo is None:
            print('Provide access token and repository https URL')
            sys.exit(1)
        clonedir = tempfile.mkdtemp()
        gh = GithubFunctions()
        gh.set_access_token(tkn)
        gh.set_base_url(source_repo)
        gh.populate_user()
        rpo = gh.clone_repo(source_repo, clonedir, 'main')
        if rpo:
            print('Successfully cloned in %s dir' % clonedir)
        else:
            print('Failed to  clone %s ' % repoUrl)


            
    
