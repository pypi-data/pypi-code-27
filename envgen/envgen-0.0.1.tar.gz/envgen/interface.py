import argparse
import colorama
from getpass import getpass
from envgen import EnvironmentGenerator
import os
import re
import urllib2

e = EnvironmentGenerator()
project_dir = ''

def valid_choice(choice):
    return isinstance(choice, (int, long))

def valid_name(name):
    if '.' in name:
        return False
    if '/' in name:
        return False
    if '\\' in name:
        return False
    if ':' in name:
        return False
    if ' ' in name:
        return False
    return True

def valid_box(box):
    m = re.compile('^([a-zA-Z0-9]|_|-)+/([a-zA-Z0-9]|_|-)+$')
    if m.match(box):
        return True
    else:
        return False

def valid_mac(mac):
    m = re.compile('^[a-fA-F0-9][a-fA-F0-9]:[a-fA-F0-9][a-fA-F0-9]:[a-fA-F0-9][a-fA-F0-9]:[a-fA-F0-9][a-fA-F0-9]:[a-fA-F0-9][a-fA-F0-9]:[a-fA-F0-9][a-fA-F0-9]$')
    if m.match(mac):
        return True
    else:
        return False

def valid_path(path):
    m = re.compile('^[a-zA-Z]:/')
    if m.match(path) and ('\\' not in path):
        return True
    else:
        return False
        
def valid_version(version):
    m = re.compile('^([0-9]+\\.)*[0-9]+$')
    if m.match(version):
        return True
    else:
        return False

def valid_vol(vol):
    m = re.compile('^(.*:)?(.*:).*$')
    if m.match(vol):
        return True
    else:
        return False

def main_menu():
    menu = 'Please choose an option: \n'
    menu += '1 - Select project to work on\n'
    menu += '2 - Show host information\n'
    menu += '3 - Quit\n'
    print menu
    choice = input('What would you like to do? [1-3]:')
    while (not valid_choice(choice)) and (choice not in range(1,4)):
        print colorama.Fore.RED + "That's not one of the choices!"
        print menu
        choice = input('What would you like to do? [1-3]:')
    return choice

def project_menu():
    projects = os.listdir(project_dir)
    menu = 'Please choose a project: \n'
    for i in range(len(projects)):
        menu += str(i+1) + ' - ' + projects[i] + '\n'
    menu += str(len(projects)+1) + ' - Create new project\n'
    menu += str(len(projects)+2) + ' - Cancel\n'
    print menu
    choice = input('Which project would you like to work on? [1-' + str(len(projects)+2) + ']:')
    while (not valid_choice(choice)) or (choice not in range(1,(len(projects)+3))):
        print colorama.Fore.RED + "That's not one of the choices!"
        print menu
        choice = input('Which project would you like to work on? [1-' + str(len(projects)+2) + ']:')
    if choice == (len(projects)+2):
        return 0
    if choice == (len(projects)+1):
        new_project = raw_input('What would you like to name your project? [String with no spaces]:')
        while not valid_name(new_project):
            print colorama.Fore.RED + "Must not contain spaces, periods, slashes, or colons"
            new_project = raw_input('What would you like to name your project? [String with no spaces]:')
        e.loadEnv(choice,project_dir+choice+'/')
        print colorama.Fore.GREEN + 'Project Created!\n'
        return 1
    else:
        e.loadEnv(projects[choice-1],project_dir+projects[choice-1]+'/')
        print colorama.Fore.GREEN + 'Project Loaded!\n'
        return 2
        
def env_menu():
    menu = 'Please choose an option:\n'
    menu += '1 - List Entities\n'
    menu += '2 - Build new Entity\n'
    menu += '3 - Edit Entities\n'
    menu += '4 - View current config\n'
    menu += '5 - Check resources\n'
    menu += '6 - Build Environment\n'
    menu += '7 - Start Environment\n'
    menu += '8 - Cancel\n'
    print menu
    choice = input('What would you like to do? [1-8]:')
    while (not valid_choice(choice)) or (choice not in range(1,9)):
        print colorama.Fore.RED + "That's not one of the choices!"
        print menu
        choice = input('What would you like to do? [1-8]:')
    if choice == 1:
        print "Environment Entitites:"
        for ent in e.workingEnv.entities:
            print ent.toString()
        return 1
    if choice == 2:
        return 2
    if choice == 3:
        return 3
    if choice == 4:
        print "Environment Config:"
        print e.workingEnv.toString()
        return 4
    if choice == 5:
        print "Checking available resources..."
        check = e.checkResources()
        if check[0] > 0:
            print colorama.Fore.RED + check[1]
        else:
            print colorama.Fore.GREEN + check[1]
        return 5
    if choice == 6:
        print "Building..."
        e.buildConfig()
        return 6
    if choice == 7:
        print "Starting Environment..."
        e.startEnv()
        return 0
    else:
        return 0

def new_entity_menu():
    mem = None
    cpu = None
    mac = None
    users = None
    software = None
    vols = None
    ports = None
    dockerfile = None
    name = raw_input('What would you like to name your entity?')
    while not valid_name(name):
        print colorama.Fore.RED + "Must not contain spaces, periods, slashes, or colons"
        name = raw_input('What would you like to name your entity?')
    os_choice = input('What type of OS is ' + name + '? [1-3]\n1 - Windows based\n2 - Unix Based\n3 - Other')
    while (not valid_choice(os_choice)) or (os_choice not in range(1,4)):
        print colorama.Fore.RED + "That's not one of the choices!"
        os_choice = input('What type of OS is ' + name + '? [1-3]\n1 - Windows based\n2 - Unix Based\n3 - Other\n')
    if os_choice == 1:
        os = 'win'
    if os_choice == 2:
        os = 'linux'
    else:
        os = 'other'
    provider_choice = input('What provider will ' + name + ' use? [1-2]\n1 - Hyper-V\n2 - Docker\n')
    while (not valid_choice(provider_choice)) or (provider_choice not in range(1,4)):
        print colorama.Fore.RED + "That's not one of the choices!"
        provider_choice = input('What provider will ' + name + ' use? [1-2]\n1 - Hyper-V\n2 - Docker\n')
    if provider_choice == 1:
        provider = 'hyperv'
    else:
        provider = 'docker'
    box = raw_input('What is the base box (Vagrant Cloud) or image (Docker Hub) that ' + name + ' will use?\nInput "None" if dockerfile will be used ')
    while (not valid_box(box)):
        if box == 'None':
            box = None
            break
        print colorama.Fore.RED + "Must be a box or image from Vagrant Cloud or Docker Hub"
        box = raw_input('What is the base box (Vagrant Cloud) or image (Docker Hub) that ' + name + ' will use? ')
    if provider == 'hyperv':
        mem = input('What are the memory requirements? [integer in MB]:\nEnter 0 for box defaults ')
        while (not valid_choice(mem)):
            if mem == 0:
                mem = None
                break
            print colorama.Fore.RED + "Must be an integer"
            mem = input('What are the memory requirements? [integer in MB]:\nEnter "None" for box defaults ')
        cpu = input('How many CPU cores? [integer]:\nEnter 0 for box defaults ')
        while (not valid_choice(cpu)):
            if cpu == 0:
                cpu = None
                break
            print colorama.Fore.RED + "Must be an integer"
            cpu = input('How many CPU cores? [integer]:\nEnter "None" for box defaults ')
        mac = raw_input('What MAC address should be used? [Format - AA:AA:AA:AA:AA:AA]:\nEnter "None" for box defaults ')
        while (not valid_mac(mac)):
            if mac == 'None':
                mac = None
                break
            print colorama.Fore.RED + "Must be in the form AA:AA:AA:AA:AA:AA"
            mac = raw_input('What MAC address should be used? [Format - AA:AA:AA:AA:AA:AA]:\nEnter "None" for box defaults ')
        user_choice = raw_input('Would you like to add custom users? [y|n]: ')
        while (user_choice != 'y') and (user_choice != 'n'):
            print colorama.Fore.RED + "Must be either 'y' or 'n'"
            user_choice = raw_input('Would you like to add custom users? [y|n]: ')
        if user_choice == 'y':
            users = user_menu()
        software_choice = raw_input('Would you like to add custom software? [y|n]: ')
        while (user_choice != 'y') and (user_choice != 'n'):
            print colorama.Fore.RED + "Must be either 'y' or 'n'"
            software_choice = raw_input('Would you like to add custom software? [y|n]: ')
        if software_choice == 'y':
            software = software_menu()
    else:
        volumes_choice = raw_input('Would you like to add shared volumes? [y|n]: ')
        while (volumes_choice != 'y') and (volumes_choice != 'n'):
            print colorama.Fore.RED + "Must be either 'y' or 'n'"
            volumes_choice = raw_input('Would you like to add shared volumes? [y|n]: ')
        if volumes_choice == 'y':
            volumes = volumes_menu()
        ports_choice = raw_input('Would you like to expose ports of your container? [y|n]: ')
        while (ports_choice != 'y') and (ports_choice != 'n'):
            print colorama.Fore.RED + "Must be either 'y' or 'n'"
            ports_choice = raw_input('Would you like to expose ports of your container? [y|n]: ')
        if ports_choice == 'y':
            ports = ports_menu()
        if box == 'None':
            dockerfile_location = raw_input('Where is the dockerfile for ' + name + ' located? [Example: C:/envgen/dockerfile]: ')
            while (not valid_path(dockerfile_location)):
                print colorama.Fore.RED + "Must be a valid path\nExample - C:/envgen/dockerfile"
                dockerfile_location = raw_input('Where is the dockerfile for ' + name + ' located? [Example: C:/envgen/dockerfile]: ')
            with open(dockerfile_location,'r') as file:
                dockerfile = file.read()
    e.buildEntity(name,box,os,provider,mem=mem, cpu=cpu, mac=mac, vols=vols, ports=ports, dockerfile=dockerfile)
    print colorama.Fore.GREEN + 'Entity Built!\n'
    
def edit_entity_menu():
    menu = 'Here are the entities to edit: \n'
    for i in range(len(e.workingEnv.entities)):
        menu += str(i+1) + ' - ' + e.workingEnv.entities[i].name + '\n'
    menu += str(len(e.workingEnv.entities)+1) + ' - Cancel\n'
    print menu
    pick = input('Which entity would you like to work on? [1-' + str(len(e.workingEnv.entities)+1) + ']:')
    while (not valid_choice(pick)) or (pick not in range(1,(len(e.workingEnv.entities)+2))):
        print colorama.Fore.RED + "That's not one of the choices!"
        print menu
        pick = input('Which entity would you like to work on? [1-' + str(len(e.workingEnv.entities)+1) + ']:')
    if pick == (len(e.workingEnv.entities)+1):
        return
    else:
        if e.workingEnv.entities[pick-1].provider == 'hyperv':
            menu = 'Here are your choices:\n'
            menu += '1 - Edit name\n'
            menu += '2 - Edit OS\n'
            menu += '3 - Edit provider\n'
            menu += '4 - Edit box name\n'
            menu += '5 - Edit memory\n'
            menu += '6 - Edit CPU cores\n'
            menu += '7 - Edit MAC address\n'
            menu += '8 - Add users\n'
            menu += '9 - Add software\n'
            menu += '10 - Delete Entity\n'
            menu += '11 - Cancel\n'
            print menu
            choice = input('What would you like to do? [1-11]: ')
            while (not valid_choice(choice)) or (choice not in range(1,12)):
                print colorama.Fore.RED + "That's not one of the choices!"
                print menu
                choice = input('What would you like to do? [1-11]: ')
            if choice == 11:
                return
            if choice == 1:
                name = raw_input('What would you like to name your entity? ')
                while not valid_name(name):
                    print colorama.Fore.RED + "Must not contain spaces, periods, slashes, or colons"
                    name = raw_input('What would you like to name your entity? ')
                e.workingEnv.entities[pick-1].name = name
            if choice == 2:
                os_choice = input('What type of OS is ' + name + '? [1-3]\n1 - Windows based\n2 - Unix Based\n3 - Other\n')
                while (not valid_choice(os_choice)) or (os_choice not in range(1,4)):
                    print colorama.Fore.RED + "That's not one of the choices!"
                    os_choice = input('What type of OS is ' + name + '? [1-3]\n1 - Windows based\n2 - Unix Based\n3 - Other\n')
                if os_choice == 1:
                    os = 'win'
                if os_choice == 2:
                    os = 'linux'
                else:
                    os = 'other'
                e.workingEnv.entities[pick-1].os = os
            if choice == 3:
                provider_choice = input('What provider will ' + name + ' use? [1-2]\n1 - Hyper-V\n2 - Docker\n')
                while (not valid_choice(provider_choice)) or (provider_choice not in range(1,3)):
                    print colorama.Fore.RED + "That's not one of the choices!"
                    provider_choice = input('What provider will ' + name + ' use? [1-2]\n1 - Hyper-V\n2 - Docker\n')
                if provider_choice == 1:
                    provider = 'hyperv'
                else:
                    provider = 'docker'
                e.workingEnv.entities[pick-1].provider = provider
            if choice == 4:
                box = raw_input('What is the base box (Vagrant Cloud) or image (Docker Hub) that ' + name + ' will use?\nInput "None" if dockerfile will be used \n')
                while (not valid_box(box)):
                    if box == 'None':
                        break
                    print colorama.Fore.RED + "Must be a box or image from Vagrant Cloud or Docker Hub"
                    box = raw_input('What is the base box (Vagrant Cloud) or image (Docker Hub) that ' + name + ' will use? \n')
                e.workingEnv.entities[pick-1].box_name = box_name
            if choice == 5:
                mem = input('What are the memory requirements? [integer in MB]:\nEnter 0 for box defaults \n')
                while (not valid_choice(mem)):
                    if mem == 0:
                        mem = None
                        break
                    print colorama.Fore.RED + "Must be an integer"
                    mem = input('What are the memory requirements? [integer in MB]:\nEnter 0 for box defaults \n')
                e.workingEnv.entities[pick-1].mem = mem
            if choice == 6:
                cpu = input('How many CPU cores? [integer]:\nEnter 0 for box defaults \n')
                while (not valid_choice(cpu)):
                    if cpu == 0:
                        cpu = None
                        break
                    print colorama.Fore.RED + "Must be an integer"
                    cpu = input('How many CPU cores? [integer]:\nEnter 0 for box defaults \n')
                e.workingEnv.entities[pick-1].cpu = cpu
            if choice == 7:
                mac = raw_input('What MAC address should be used? [Format - AA:AA:AA:AA:AA:AA]:\nEnter "None" for box defaults \n')
                while (not valid_mac(mac)):
                    if mac == 'None':
                        mac = None
                        break
                    print colorama.Fore.RED + "Must be in the form AA:AA:AA:AA:AA:AA"
                    mac = raw_input('What MAC address should be used? [Format - AA:AA:AA:AA:AA:AA]:\nEnter "None" for box defaults \n')
                e.workingEnv.entities[pick-1].mac = mac
            if choice == 8:
                users = user_menu(users=e.workingEnv.entities[pick-1].users)
                e.workingEnv.entities[pick-1].users = users
            if choice == 9:
                software = software_menu(software=e.workingEnv.entities[pick-1].software)
                e.workingEnv.entities[pick-1].software = software
            if choice == 10:
                e.removeEntity(e.workingEnv.entities[pick-1].name)
        else:
            menu = 'Here are your choices:\n'
            menu += '1 - Edit name\n'
            menu += '2 - Edit OS\n'
            menu += '3 - Edit provider\n'
            menu += '4 - Edit image name\n'
            menu += '5 - Edit volumes\n'
            menu += '6 - Edit ports\n'
            menu += '7 - Edit dockerfile\n'
            menu += '8 - Delete Entity\n'
            menu += '9 - Cancel\n'
            print menu
            choice = input('What would you like to do? [1-9]: ')
            while (not valid_choice(choice)) or (choice not in range(1,10)):
                print colorama.Fore.RED + "That's not one of the choices!"
                print menu
                choice = input('What would you like to do? [1-9]: ')
            if choice == 9:
                return
            if choice == 1:
                name = raw_input('What would you like to name your entity? ')
                while not valid_name(name):
                    print colorama.Fore.RED + "Must not contain spaces, periods, slashes, or colons"
                    name = raw_input('What would you like to name your entity? ')
                e.workingEnv.entities[pick-1].name = name
            if choice == 2:
                os_choice = input('What type of OS is ' + name + '? [1-3]\n1 - Windows based\n2 - Unix Based\n3 - Other\n')
                while (not valid_choice(os_choice)) or (os_choice not in range(1,4)):
                    print colorama.Fore.RED + "That's not one of the choices!"
                    os_choice = input('What type of OS is ' + name + '? [1-3]\n1 - Windows based\n2 - Unix Based\n3 - Other\n')
                if os_choice == 1:
                    os = 'win'
                if os_choice == 2:
                    os = 'linux'
                else:
                    os = 'other'
                e.workingEnv.entities[pick-1].os = os
            if choice == 3:
                provider_choice = input('What provider will ' + name + ' use? [1-2]\n1 - Hyper-V\n2 - Docker\n')
                while (not valid_choice(provider_choice)) or (provider_choice not in range(1,3)):
                    print colorama.Fore.RED + "That's not one of the choices!"
                    provider_choice = input('What provider will ' + name + ' use? [1-2]\n1 - Hyper-V\n2 - Docker\n')
                if provider_choice == 1:
                    provider = 'hyperv'
                else:
                    provider = 'docker'
                e.workingEnv.entities[pick-1].provider = provider
            if choice == 4:
                box = raw_input('What is the base box (Vagrant Cloud) or image (Docker Hub) that ' + name + ' will use?\nInput "None" if dockerfile will be used \n')
                while (not valid_box(box)):
                    if box == 'None':
                        box = None
                        break
                    print colorama.Fore.RED + "Must be a box or image from Vagrant Cloud or Docker Hub"
                    box = input('What is the base box (Vagrant Cloud) or image (Docker Hub) that ' + name + ' will use? \n')
                e.workingEnv.entities[pick-1].box_name = box_name
            if choice == 5:
                volumes = volumes_menu(vols=e.workingEnv.entities[pick-1].vols)
                e.workingEnv.entities[pick-1].vols = volumes
            if choice == 6:
                ports = ports_menu(ports=e.workingEnv.entities[pick-1].ports)
                e.workingEnv.entities[pick-1].ports = ports
            if choice == 7:
                dockerfile_location = raw_input('Where is the dockerfile for ' + name + ' located? [Example: C:/envgen/dockerfile]: ')
                while (not valid_path(dockerfile_location)):
                    print colorama.Fore.RED + "Must be a valid path\nExample - C:/envgen/dockerfile"
                    dockerfile_location = raw_input('Where is the dockerfile for ' + name + ' located? [Example: C:/envgen/dockerfile]: ')
                with open(dockerfile_location,'r') as file:
                    dockerfile = file.read()
                e.workingEnv.entities[pick-1].box_name = 'None'
                e.workingEnv.entities[pick-1].dockerfile = dockerfile
            if choice == 8:
                e.removeEntity(e.workingEnv.entities[pick-1].name)
    print colorama.Fore.GREEN + 'Entity Updated!\n'
        
def user_menu(users=None):
    if users is None:   
        users = []
    num_to_add = input('How many users do you want to add? [integer]: ')
    while (not valid_choice(num_to_add)):
        print colorama.Fore.RED + "Must be an integer"
        num_to_add = input('How many users do you want to add? [integer]: ')
    for i in range(num_to_add): 
        print "User #" +str(i+1)
        user = raw_input('Username? [String]: ')
        while (not valid_name(user)):
            print colorama.Fore.RED + "Must not contain spaces, periods, slashes, or colons"
            user = raw_input('Username? [String]: ')
        pw = getpass('Password? [String]: ')
        users.append((user,pw))
    return users
    
def software_menu(software=None):
    if software is None:   
        software = []
    num_to_add = input('How many puppet modules (Puppet Forge) do you want to add? [integer]: ')
    while (not valid_choice(num_to_add)):
        print colorama.Fore.RED + "Must be an integer"
        num_to_add = input('How many puppet modules do you want to add? [integer]: ')
    for i in range(num_to_add): 
        print "Module #" +str(i+1)
        mod = raw_input('Module? [From Puppet Forge]: ')
        while (not valid_box(mod)):
            print colorama.Fore.RED + "Must be a module from Puppet Forge"
            mod = raw_input('Module? [From Puppet Forge]: ')
        version = raw_input('What version do you want to use? [Enter "None" for latest]: ')
        while (not valid_version(version)):
            if version == 'None':
                version = None
                break
            print raw_colorama.Fore.RED + "Must be a valid version"
            version = raw_input('What version do you want to use? [Enter "None" for latest]: ')
        software.append((mod,version))
    return software
    
def volumes_menu(vols=None):
    if vols is None:   
        vols = []
    num_to_add = input('How many volumes do you want to add? [integer]: ')
    while (not valid_choice(num_to_add)):
        print colorama.Fore.RED + "Must be an integer"
        num_to_add = input('How many volumes do you want to add? [integer]: ')
    for i in range(num_to_add): 
        print "Volume #" +str(i+1)
        vol = raw_input('Volume? [Docker format for volume declaration]: ')
        while (not valid_vol(vol)):
            print colorama.Fore.RED + "Must in valid Docker volume format"
            vol = raw_input('Volume? [Docker format for volume declaration]: ')
        vols.append(vol)
    return vols
    
def ports_menu(ports=None):
    if ports is None:   
        ports = []
    num_to_add = input('How many ports do you want to add? [integer]: ')
    while (not valid_choice(num_to_add)):
        print colorama.Fore.RED + "Must be an integer"
        num_to_add = input('How many ports do you want to add? [integer]: ')
    for i in range(num_to_add): 
        print "Port #" +str(i+1)
        port = raw_input('Port? [Docker format for exposing ports]: ')
        while (not valid_vol(port)):
            print colorama.Fore.RED + "Must in valid Docker expose port format"
            port = raw_input('Port? [Docker format for exposing ports]: ')
        ports.append(port)
    return ports

def main():
    parser = argparse.ArgumentParser(description='Runs the Text Interface for the Environment Generator')
    parser.add_argument('project_dir', metavar='Project_Directory', help='Define the project directory.  End with forward slash(/).\nExample: C:/envgen/projects/')
    args = parser.parse_args()
    global project_dir
    project_dir = args.project_dir
    intro = urllib2.urlopen('https://raw.githubusercontent.com/jonebeabout/envgen/master/envgen/envgen/ascii_art.txt').read()
    intro += '\nWelcome to the Environment Generator!\n'
    intro += 'Use this tool to generate virtual networks that can be used for simulation and exploratory learning and fuel flipped learning in the classroom.'
    intro += '\n\n'
    print intro
    colorama.init(autoreset=True)
    no_exit = True
    in_project = False
    while(no_exit):
        if not in_project:
            result = main_menu()
        else:
            result = 1
        if result == 1:
            result = project_menu()
            if result == 0:
                in_project = False
                continue
            else:
                result = env_menu()
                while result > 0:
                    if result == 2:
                        new_entity_menu()
                    if result == 3:
                        edit_entity_menu()
                    result = env_menu()
                if result == 0:
                    in_project = True
                    continue        
        if result == 2:
            e.host = e.updateHost()
            print e.host.toString()
            continue
        else:   
            no_exit = False
    colorama.deinit()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs the Text Interface for the Environment Generator')
    parser.add_argument('project_dir', metavar='Project_Directory', help='Define the project directory.  End with forward slash(/).\nExample: C:/envgen/projects/')
    args = parser.parse_args()
    project_dir = args.project_dir
    intro = urllib2.urlopen('https://raw.githubusercontent.com/jonebeabout/envgen/master/envgen/envgen/ascii_art.txt').read()
    intro += '\nWelcome to the Environment Generator!\n'
    intro += 'Use this tool to generate virtual networks that can be used for simulation and exploratory learning and fuel flipped learning in the classroom.'
    intro += '\n\n'
    print intro
    
    colorama.init(autoreset=True)
    no_exit = True
    in_project = False
    while(no_exit):
        if not in_project:
            result = main_menu()
        else:
            result = 1
        if result == 1:
            result = project_menu()
            if result == 0:
                in_project = False
                continue
            else:
                result = env_menu()
                while result > 0:
                    if result == 2:
                        new_entity_menu()
                    if result == 3:
                        edit_entity_menu()
                    result = env_menu()
                if result == 0:
                    in_project = True
                    continue        
        if result == 2:
            e.host = e.updateHost()
            print e.host.toString()
            continue
        else:   
            no_exit = False
    colorama.deinit()











