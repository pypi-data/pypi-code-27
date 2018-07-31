import os
import os.path as iou
import gnupg
import splogger as log
import getpass
from colorama import Fore
from os import listdir, sep
from os.path import abspath, basename, isdir
from subprocess import Popen, CalledProcessError
import json
import shutil


PADLOCK         = '🔒'
OPEN_PADLOCK    = '🔓'
JOURNAL_ROOT    = '/home/'+getpass.getuser()+'/.nikki'
INDEX_FILENAME  = '.index'
PASSWORD        = None # FIXME unsafe ?
INDEX           = {}

STATUS_NONE         = 0
STATUS_INITIALIZED  = 1
STATUS_DECRYPTED    = 2

def require_status(status):
    """
    Check if the required status is met for the program to start
    """
    # log.set_verbose(True)
    if status >= 1:
        if not iou.isfile(iou.join(JOURNAL_ROOT, INDEX_FILENAME)):
            log.error(Fore.RED+'The journal is not initialized'+Fore.RESET)
            log.error(Fore.RED+'Run nikki init first'+Fore.RESET)
            exit(1)
        os.chdir(JOURNAL_ROOT)
    
    if status >= 2:
        get_pass()
        decrypt_journal()
  

def get_pass():
    """
    Ask for the password and try to decrypt the 
    """ 

    global INDEX
    global PASSWORD

    crypt = None
    gpg = gnupg.GPG()

    index_crypt = None
    with open(iou.join(JOURNAL_ROOT, INDEX_FILENAME), 'r') as ifh:
        index_crypt = ifh.read()

    while True:
        passphrase = getpass.getpass('Enter the password to access the journal: ')
        crypt = gpg.decrypt(index_crypt, passphrase = passphrase)

        if not crypt.ok:
            log.error(Fore.RED + PADLOCK + '  Could not unlock the journal, is the passphrase correct?'+Fore.RESET)
        else:
            break
    
    INDEX = crypt
    PASSWORD = passphrase

@log.element('Decrypting the journal')
def decrypt_journal():
    gpg = gnupg.GPG()
    for current_dir, _, files in os.walk(JOURNAL_ROOT):
        for filename in files:
            if filename == INDEX_FILENAME:
                continue
            log.set_additional_info(filename)

            with open(iou.join(current_dir, filename), 'r') as frh:
                file_crypted = frh.read()

            file_clear = gpg.decrypt(file_crypted, passphrase = PASSWORD)
            if not file_clear.ok:
                log.error('Cannot decrypt '+filename)
                continue
            file_clear = file_clear.data

            with open(iou.join(current_dir, filename), 'w+') as fwh:
                fwh.write(file_clear.decode('utf-8'))


@log.element('Encrypting the journal')
def encrypt_journal():
    gpg = gnupg.GPG()
    for current_dir, _, files in os.walk(JOURNAL_ROOT):
        for filename in files:
            log.set_additional_info(filename)

            with open(iou.join(current_dir, filename), 'r') as frh:
                file_clear = frh.read()

            gpg.encrypt(file_clear, (), symmetric = True, passphrase = PASSWORD, output=iou.join(current_dir, filename))
    log.success(Fore.GREEN + PADLOCK + '  Journal secured' + Fore.RESET)

"""
From https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
"""
def tree(dir, padding, print_files=False, isLast=False, isFirst=False):
    if isFirst:
        print(padding[:-1] + dir)
    else:
        if isLast:
            print(padding[:-1] + '└── ' + basename(abspath(dir)))
        else:
            print(padding[:-1] + '├── ' + basename(abspath(dir)))
    files = []
    if print_files:
        files = listdir(dir)
    else:
        files = [x for x in listdir(dir) if isdir(dir + sep + x)]
    if not isFirst:
        padding = padding + '   '
    files = sorted(files, key=lambda s: s.lower())
    count = 0
    last = len(files) - 1
    for i, file in enumerate(files):
        count += 1
        path = dir + sep + file
        isLast = i == last
        if isdir(path):
            if count == len(files):
                if isFirst:
                    tree(path, padding, print_files, isLast, False)
                else:
                    tree(path, padding + ' ', print_files, isLast, False)
            else:
                tree(path, padding + '│', print_files, isLast, False)
        else:
            if isLast:
                print(padding + '└── ' + file)
            else:
                print(padding + '├── ' + file)

def print_journal():
    tree(JOURNAL_ROOT, '')

def git_call(args):
    os.chdir(JOURNAL_ROOT)
    log.debug('Call git: '+str(args))
    with Popen(['git', *args]) as p:
        p.wait() 

def add_entry(path):
    p = ' '.join(path).split('/')
    os.makedirs(iou.join(JOURNAL_ROOT, *p), exist_ok = True)
    log.success('Added entry: '+str(*path))

def remove_entry(path, confirm = True):
    if confirm:
        yes = input('Enter "YES" to confirm the deletion of '+path+' : ')
        if yes != "YES":
            log.error('Aborted')
            exit(1)
    os.rmdir(iou.join(JOURNAL_ROOT, path))

def edit(path):
    path = ' '.join(path)
    if not iou.isfile(iou.join(JOURNAL_ROOT, path)):
        log.warning('Creating new entry: '+path)
       
    
    log.success('Edit: '+path)
    open_editor(iou.join(JOURNAL_ROOT, path))

## NB: The index is loaded in ask_pass
def save_index():
    gpg = gnupg.GPG()
    gpg.encrypt(json.dumps(INDEX), (), symmetric=True, passphrase = PASSWORD, output=iou.join(JOURNAL_ROOT, INDEX_FILENAME))

def init_journal():
    global PASSWORD
    if iou.isfile(iou.join(JOURNAL_ROOT, INDEX_FILENAME)):  
        log.warning(Fore.YELLOW+'WARNING: This operation will delete the current journal and the git structure !'+Fore.RESET)
        yes = input('Enter "YES" to confirm the operation: ')
        if yes != "YES":
            log.error('Aborted')
            exit(1)
        shutil.rmtree(JOURNAL_ROOT)
    
    os.makedirs(JOURNAL_ROOT, exist_ok = True)
    while True:
        pp = getpass.getpass('Enter passphrase for journal:')
        pp2 = getpass.getpass('Confirm passphrase:')

        if pp == pp2:
            PASSWORD = pp
            save_index()
            break

        log.error('Passphrases do not match')
    log.success(Fore.GREEN+'Journal initilized in '+JOURNAL_ROOT+Fore.RESET)


def open_editor(filename):
    os.system('%s %s' % (os.getenv('EDITOR'), filename))