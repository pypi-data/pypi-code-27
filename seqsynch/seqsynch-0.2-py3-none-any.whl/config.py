# -*- coding: utf-8 -*-
"""
@author: mezeda01
Configurations script file with helper functions"""

import os
import time
import datetime
from git import Repo, Git
import git
import logging
from configparser import ConfigParser

# Global variable to know when do we have to do a hard reset on the tree
do_hard = False

def create_loggers(log_name):
    '''returns 3 loggers whith decreasing priority, and configures the logging
    according to the log filename'''
    formatter = logging.Formatter('%(asctime)s\t%(name)s:%(levelname)s\t%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logging.basicConfig(filename=log_name,
                        level=logging.INFO,
                        format="%(asctime)s\t%(name)s:%(levelname)s\t%(message)s")
    logger = logging.getLogger('log1')
    #The loggers message should printed as well
    logger.addHandler(ch)
    return logger

def get_globals():
    '''returns global variables for the main script'''
    config = ConfigParser()
    config.read('config.ini')
    if len(config.sections())==0:
        raise Exception('Empty or non-existing config.ini file!')
    else:
        comment_ch = ';'
        USERNAME = config.get('names', 'username').split(comment_ch, 1)[0].strip()
        CENTERNAME = config.get('names', 'centername').split(comment_ch, 1)[0].strip()
        REPO_NAME = config.get('names', 'repo_name').split(comment_ch, 1)[0].strip()
        DEST_NAME = config.get('names', 'dest_name').split(comment_ch, 1)[0].strip()
        SSH_KEY = config.get('ssh', 'ssh_key').split(comment_ch, 1)[0].strip()
        # the key needs to be generated according to GitHub's suggestions in root .ssh dir
        SSH_KEY = '~/.ssh/'+SSH_KEY
        PULL_CYCLE = float(config.get('pull', 'pull_cycle').split(comment_ch, 1)[0].strip())
        PUSH_CYCLE = float(config.get('push', 'push_cycle').split(comment_ch, 1)[0].strip())
        PUSH_SWITCH = config.get('push', 'push_switch').split(comment_ch, 1)[0].strip() == 'True'
        # Address to clone from (SSH)
        SSH_CLONE_ADR = 'git@github.com:{}/{}.git'.format(USERNAME,REPO_NAME)
        # SSH command for git
        SSH_CMD = 'ssh -i {}'.format(SSH_KEY)
        # Log file name
        LOG_NAME = 'log_{}.txt'.format(CENTERNAME)
        return USERNAME, CENTERNAME, REPO_NAME, REPO_NAME, SSH_CLONE_ADR, DEST_NAME, SSH_KEY,SSH_CMD, PULL_CYCLE, PUSH_SWITCH, PUSH_CYCLE, LOG_NAME

def timestamp():
    '''generates a human readable timestamp for comments and commits'''
    timestamp = time.time()
    value = datetime.datetime.fromtimestamp(timestamp)
    return value.strftime('%H:%M:%S_%Y%m%d')

def checkout_branch(repo, branchname):
    '''Checking if there exists a given branch and checking out to it.
    For future use only'''
    print('Repo check out...\t\t\t', end='', flush=True)
    # getting all branch names
    branches = [head.name for head in repo.heads]
    if branchname in branches:
        # A branch with the given branch name exists
        repo.git.checkout(branchname)
    else:
        # No existing branch with the branchname, so let's create one
        repo.create_head(branchname)
        repo.git.checkout(branchname)
    print('finished!')

def listen(repo, log1, dest_name, centername):
    '''listening for changes in local repository. Either changed or added untracked_files
    files'''
    global do_push
    #listening for changes
    changed = check_diff(repo)
    # listening for new files
    added = check_new(repo)
    do_push = False
    # generating commit message accordingly
    if changed:
        if added:
            #there are new and changed files as well
            log1.info('Some files have been changed and added.')
            # adding everything to the commit except file removals
            # the CITB user has no rights to delete anything permanently
            add_all(repo,['--ignore-removal','{}/{}'.format(os.getcwd(), dest_name)])
            message = '{} -> Changes and new files commited'.format(centername)
            commit_all(repo,message)
            # we made a new commit so we should push it
            do_push = True
            log1.info('Commited with message: {}'.format(message))
            return True
        else:
            #there are some files which are changed
            log1.info('Some files have been changed.')
            # adding everything to the commit except file removals
            # the CITB user has no rights to delete anything permanently
            add_all(repo,['--ignore-removal','{}/{}'.format(os.getcwd(), dest_name)])
            message = '{} -> Changes commited'.format(centername)
            commit_all(repo,message)
            # we made a new commit so we should push it
            do_push = True
            log1.info('Commited with message: {}'.format(message))
            return True
    else:
        if added:
            #there are some files which are changed
            log1.info('Some files have been added.')
            untracked = ', '.join(repo.untracked_files)
            numuntracked = len(repo.untracked_files)
            #  adding everything to the commit except file removals
            # the CITB user has no rights to delete anything permanently
            add_all(repo,['--ignore-removal','{}/{}'.format(os.getcwd(), dest_name)])
            message = '{} -> {} new files added : new files: {}'.format(centername, numuntracked,
                                                                        untracked)
            commit_all(repo,message)
            # the new commit needs to be pushed
            do_push = True
            log1.info('Commited with message: {}'.format(message))
            return True
        else:
            log1.info('Listener returned with False : No changes sincle last cycle')
            return False

def auto_pull(repo, log1):
    '''single pull cycle, scheduled for every X seconds'''
    global do_hard # hard or mixed reset for pulling the origin (we also want to write)
    log1.info('PULL cycle waking up')
    time.sleep(1)
    # pull everything
    log1.info('Pulling repo...')
    if do_hard:
        #in this case in the last cycle there was a push, so we can reset our
        #tree to the current origin one
        log1.info('Hard reset of working tree')
        repo.git.reset('--hard')
        # flipping do_hard, so next time we do not make a hard reset, except
        # some changes happen and we commit and push them
        do_hard = False
    else:
        # in this case we are doing a mixed reset, the changed files which has not
        # yet been commited will not be reset
        log1.info('Mixed reset of working tree')
        repo.git.reset('--mixed')
    # now we can pull according to the tree reset
    repo.remotes.origin.pull('master')
    log1.info('PULL cycle falling asleep')

def auto_push(repo, log1, ssh_cmd):
    '''single push cycle scheduled for every X seconds'''
    global do_hard
    if do_push:
        repo.remotes.origin.push('master')
        log1.info('Commited changes pushed.')
        # we pushed something so we can do a hard reset next time on our tree
        do_hard = True

def add_all(repo, flag):
    '''Adding changed or new files to the next commit from repo according to flag
    flag = -u : local changes and deletions, no adding files
    flag = -A : all local changes also untracked files
    flag = ['--ignore-removal',<local repo path>]: ignores deletions'''
    repo.git.add(flag)

def commit_all(repo, message):
    '''Creating a commit from repo with given message'''
    repo.index.commit(message)

def check_diff(repo):
    '''Checking for changed files'''
    is_diff = False
    if repo.git.diff()!='':
        is_diff = True
    return is_diff

def check_new(repo):
    '''Checking for new, untracked files'''
    is_there_new = False
    if len(repo.untracked_files)>0:
        is_there_new = True
    return is_there_new
