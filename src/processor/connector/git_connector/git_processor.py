import os
import re
import tempfile
import urllib.parse
import stat
from subprocess import Popen, PIPE
from processor.connector.git_connector.git_functions import GithubFunctions, check_clone_repos, set_clone_repo
from processor.helper.file.file_utils import exists_file, exists_dir
from processor.helper.json.json_utils import get_field_value, get_field_value_with_default
from processor.logging.log_handler import getlogger
from processor.helper.config.rundata_utils import get_from_currentdata
from processor.connector.vault import get_vault_data

logger = getlogger()

def create_ssh_file_vault_data(ssh_dir, ssh_key_file_data, ssh_fname):
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL  # Refer to "man 2 open".
    mode = stat.S_IRUSR | stat.S_IWUSR
    umask = 0o777 ^ mode
    umask_original = os.umask(umask)
    ssh_key_file = '%s/%s' % (ssh_dir, ssh_fname)
    try:
        fdesc = os.open(ssh_key_file, flags, mode)
        with os.fdopen(fdesc, 'w') as fout:
            for l in  ssh_key_file_data.split('\\n'):
                fout.write(l + '\n')
    finally:
        os.umask(umask_original)
    return ssh_key_file

def run_subprocess_cmd(cmd, ignoreerror=False, maskoutput=False, outputmask="Error output is masked"):
    """ Run a sub-process command"""
    result = ''
    errresult = None
    if cmd:
        if isinstance(cmd, list):
            cmd = ' '.join(cmd)
        myprocess = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        out, err = myprocess.communicate()
        result = out.rstrip()
        errresult = err.rstrip() if err else None
        if isinstance(result, bytes):
            result = result.decode()
        if errresult and isinstance(errresult, bytes):
            errresult = errresult.decode()
    return errresult, result

def create_ssh_config(ssh_dir, ssh_key_file, ssh_user):
    ssh_config = '%s/config' % ssh_dir
    if exists_file(ssh_config):
        logger.error("Git config: %s already exists, cannot modify it!")
        return None
    with open(ssh_config, 'w') as f:
        f.write('Host *\n')
        # f.write('Host %s\n' % ssh_host)
        # f.write('   HostName %s\n' % ssh_host)
        f.write('   User %s\n' % ssh_user)
        f.write('   IdentityFile %s\n\n' % ssh_key_file)
        # f.write('Host *\n')
        f.write('   IdentitiesOnly yes\n')
        f.write('   ServerAliveInterval 100\n')
    return ssh_config

def get_pwd_from_vault(password_key):
    """ Return the git password from vault """
    password = get_vault_data(password_key)
    if not password:
        logger.info("Password does not set in the vault")
    return password

def get_git_pwd(key='GIT_PWD'):
    """ Return the git password for https connection"""
    git_pwd = get_from_currentdata('GIT_PWD')
    if not git_pwd:
        git_pwd = os.getenv(key, None)
        if git_pwd:
            logger.info("Git password from envirnment: %s", '*' * len(git_pwd))
    return git_pwd

def git_clone_dir(connector, giturl=None, branch=None, clone_specific_branch=True):
    global CLONE_REPOS
    clonedir = None
    repopath = tempfile.mkdtemp()
    subdir = False
    if connector and isinstance(connector, dict):
        if not giturl:
            giturl = get_field_value(connector, 'gitProvider')
            if not giturl:
                logger.error("Git connector does not have valid git provider URL")
                return repopath, clonedir
        
        if not branch and clone_specific_branch:
            # Removed command line option for branch
            branch = get_field_value_with_default(connector, 'branchName', 'master')
            # branch = get_from_currentdata('branch')
            # if not branch:
            #     branch = get_field_value_with_default(connector, 'branchName', 'master')

        isprivate = get_field_value(connector, 'private')
        isprivate = True if isprivate is None or not isinstance(isprivate, bool) else isprivate
        # logger.info("Repopath: %s", repopath)
        logger.info("\t\t\tRepopath: %s", repopath)
        http_match = re.match(r'^http(s)?://', giturl, re.I)
        if http_match:
            logger.info("\t\t\tHttp (private:%s) giturl: %s", "YES" if isprivate else "NO", giturl)

            accessToken = get_field_value(connector, 'httpsAccessToken')
            username = get_field_value(connector, 'httpsUser')
            if accessToken:
                logger.info("AccessToken: %s" % accessToken)
                pwd = get_field_value(connector, 'httpsPassword')
                isremote = get_from_currentdata('remote')
                if isremote:
                    gittoken = get_from_currentdata('gittoken')
                    pwd = gittoken if gittoken else None
                pwd = pwd if pwd else get_git_pwd(key=accessToken)
                if not pwd:
                    pwd = get_pwd_from_vault(accessToken)
                    if pwd:
                        logger.info("Git access token from vault: %s", '*' * len(pwd))
                if pwd:
                    gh = GithubFunctions()
                    gh.set_base_url(giturl)
                    gh.set_access_token(pwd)
                    _ = gh.populate_user()
                    rpo = gh.clone_repo(giturl, repopath, branch)
                    if rpo:
                        logger.info('Successfully cloned in %s dir' % repopath)
                        checkdir = '%s/tmpclone' % repopath if subdir else repopath
                        clonedir = checkdir if exists_dir('%s/.git' % checkdir) else None
                        if not exists_dir(clonedir):
                            logger.error("No valid data provided for connect to git : %s", giturl)
                        return repopath, clonedir
                    elif isprivate:
                        logger.error("Please provide password for connect to git repository.")
                        return repopath, clonedir
                    else:
                        git_cmd = 'git clone %s %s' % (giturl, repopath)
            elif username:
                pwd = get_field_value(connector, 'httpsPassword')
                schema = giturl[:http_match.span()[-1]]
                other_part = giturl[http_match.span()[-1]:]
                # pwd = pwd if (pwd and not json_source()) else (get_git_pwd() if not json_source() else get_pwd_from_vault(pwd))
                pwd = pwd if pwd else get_git_pwd(key=username)

                # populate the password from vault
                if not pwd:
                    pwd = get_pwd_from_vault(username)
                    if pwd:
                        logger.info("Git password from vault: %s", '*' * len(pwd))
                if pwd:
                    git_cmd = 'git clone --depth 1 %s%s:%s@%s %s' % (schema, urllib.parse.quote_plus(username),
                                                        urllib.parse.quote_plus(pwd), other_part, repopath)
                elif isprivate:
                    logger.error("Please provide password for connect to git repository.")
                    return repopath, clonedir
                else:
                    git_cmd = 'git clone --depth 1 %s%s:%s@%s %s' % (schema, urllib.parse.quote_plus(username), "",
                                                     other_part, repopath)
            else:
                git_cmd = 'git clone --depth 1 %s %s' % (giturl, repopath)
        else:
            logger.info("SSH (private:%s) giturl: %s, Repopath: %s", "YES" if isprivate else "NO",
                        giturl, repopath)
            if isprivate:
                ssh_key_file = get_field_value(connector, 'sshKeyfile')
                ssh_key_name = get_field_value(connector, 'sshKeyName')
                ssh_key_file_data = None
                if ssh_key_file:
                    if not exists_file(ssh_key_file):
                        logger.error("Git connector points to a non-existent ssh keyfile!")
                        return repopath, clonedir
                elif ssh_key_name:
                    ssh_key_file_data = get_vault_data(ssh_key_name)
                    if not ssh_key_file_data:
                        logger.info('Git connector points to a non-existent ssh keyName in the vault!')
                        return repopath, clonedir
                ssh_host = get_field_value(connector, 'sshHost')
                ssh_user = get_field_value_with_default(connector, 'sshUser', 'git')
                if not ssh_host:
                    logger.error("SSH host not set, could be like github.com, gitlab.com, 192.168.1.45 etc")
                    return repopath, clonedir
                ssh_dir = '%s/.ssh' % repopath
                if exists_dir(ssh_dir):
                    logger.error("Git ssh dir: %s already exists, cannot recreate it!", ssh_dir)
                    return repopath, clonedir
                os.mkdir('%s/.ssh' % repopath, 0o700)
                if not ssh_key_file and ssh_key_name and ssh_key_file_data:
                    ssh_key_file = create_ssh_file_vault_data(ssh_dir, ssh_key_file_data, ssh_key_name)
                    if not ssh_key_file:
                        logger.info('Git connector points to a non-existent ssh keyName in the vault!')
                        return repopath, clonedir
                ssh_cfg = create_ssh_config(ssh_dir, ssh_key_file, ssh_user)
                if not ssh_cfg:
                    logger.error("Creation of Git ssh config in dir: %s failed!", ssh_dir)
                    return repopath, clonedir
                git_ssh_cmd = 'ssh -o "StrictHostKeyChecking=no" -F %s' % ssh_cfg
                git_cmd = 'git clone %s %s/tmpclone' % (giturl, repopath)
                subdir = True
            else:
                git_ssh_cmd = 'ssh -o "StrictHostKeyChecking=no"'
                git_cmd = 'git clone %s %s' % (giturl, repopath)
            os.environ['GIT_SSH_COMMAND'] = git_ssh_cmd
        
        if branch:
            git_cmd = '%s --branch %s' % (git_cmd, branch)
        
        if git_cmd:
            re_path, cln_dir = check_clone_repos(git_cmd=git_cmd.replace(repopath, ""))
            if re_path and cln_dir:
                return re_path, cln_dir
            error_result, result = run_subprocess_cmd(git_cmd)
            checkdir = '%s/tmpclone' % repopath if subdir else repopath
            clonedir = checkdir if exists_dir('%s/.git' % checkdir) else None
            if not exists_dir(clonedir):
                logger.error("No valid data provided for connect to git : %s", error_result)
            else:
                set_clone_repo(git_cmd.replace(repopath, ""), repopath, clonedir)
        if 'GIT_SSH_COMMAND' in os.environ:
            os.environ.pop('GIT_SSH_COMMAND')
    return repopath, clonedir
