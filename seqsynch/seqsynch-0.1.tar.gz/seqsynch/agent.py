# -*- coding: utf-8 -*-
"""
@author: mezeda01
v0.0 prototype for git synch tool for sequence management

agent script file"""

import os
import time
import datetime
import schedule
from git import Repo, Git
import git
import logging

from . import config as conf

do_hard = False

# Global variables from config
username, centername, repo_name, repo_name, ssh_clone_adr, dest_name, ssh_key, ssh_cmd, pull_c_freq, push_c_freq, log_name = conf.get_globals()

# Creating loggers for logging in file
log1 = conf.create_loggers(log_name)

def main():
    # INITIALIZATION
    os.system('ssh-add {}'.format(ssh_key))
    #Try to clone the folder via SSH
    try:
        with Git().custom_environment(GIT_SSH_COMMAND=ssh_cmd):
            repo = Repo.clone_from(ssh_clone_adr, dest_name)
            log1.info('Cloning from origin...')
    except git.GitCommandError as e:
        if e.status==128:
            # if there exists a clone we should pull the most recent version
            log1.info('Already existing clone! Initializing...')
            repo = Repo.init(dest_name)
            # ALL UNSTAGED LOCAL CHANGES WILL BE LOST,
            # but that's fine because there exists a push from previous run
            # and we suppose there is no new file between runs
            repo.git.reset('--hard')
            # Pull all changes from origin to master
            repo.remotes.origin.pull('master')
            log1.info('Repo pulled from remote master to local branch {}!\n'.format(repo.active_branch))
        else:
            log1.error('Unknown error during initializing repository:\n')
            log1.info('Original error message: \n\n')
            log1.info(e.stderr)

    def listen_commit_push():
        conf.listen(repo, log1, dest_name, centername)
        conf.auto_push(repo, log1, ssh_cmd)

    def pull_cycle():
        conf.auto_pull(repo, log1)

    schedule.every(pull_c_freq).seconds.do(pull_cycle)
    schedule.every(push_c_freq).seconds.do(listen_commit_push)

    try:
        while True:
            schedule.run_pending()
            time.sleep(0.25)
    except KeyboardInterrupt:
        log1.warn('Agent is being terminated by user...')
        log1.info('Finalizing')
        pull_cycle()
        log1.info('Agent terminated!')
