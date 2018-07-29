import os
import psutil
import socket
import vagrant
import colorama
import re

class Host:
    
    def __init__(self, hname, mem, dsk, cpu):
        self.hostname = hname #str
        self.memory = mem #(total[long],available[long],percent[double],used[long],free[long])
        self.disk = dsk #array of (volume_name[str],(total[long],used[long],free[long],percent[double])) for each volume
        self.cpu = cpu #(cpu_utilization, cpu_cores)
        
    def calcTotalDisk(self):
        total = 0
        used = 0
        for dsk in self.disk:
            total += dsk[1][0]
            used += dsk[1][1]
        percentage = float(used) / total * 100
        return (total, percentage)
        
    def toString(self):
        diskInfo = self.calcTotalDisk()
        rtn = 'Host Information:\n'
        rtn += '\tHostname: ' + self.hostname + '\n'
        rtn += '\tCPU Utilization: ' + str(self.cpu[0]) + '%\tCPU Cores Available: ' + str(self.cpu[1]) + '\n'
        rtn += '\tMemory Usage: Total Available - ' + str(self.memory[0]/1024/1024/1024) + 'GB\tPercent Used - ' + str(self.memory[2]) + '%\n'
        rtn += '\tDisk Usage: Total Available - ' + str(diskInfo[0]/1024/1024/1024) + 'GB\tPercent Used - ' + ("%.2f" % diskInfo[1]) + '%\n'
        for dsk in self.disk:
            rtn += '\t\t' + dsk[0] + ' Drive: Total Available - ' + str(dsk[1][0]/1024/1024/1024) + 'GB\tPercent Used - ' + str(dsk[1][3]) + '%\n'
        return rtn

class Entity:
    
    def __init__(self, name, box_name, os, provider, users=None, software=None, mem=None, cpu=None, mac=None, vols=None, ports=None, dockerfile=None):
        self.name = name
        self.os = os
        self.provider = provider
        self.mem = mem
        self.cpu = cpu
        self.mac = mac
        if users:
            self.users = users
        else:
            self.users = []
        if software:
            self.software = software
        else:
            self.software = []
        if vols:
            self.vols = vols
        else:
            self.vols = []
        if ports:
            self.ports = ports
        else:
            self.ports = []
        if dockerfile:
            self.dockerfile = dockerfile
        else:
            self.dockerfile = ''
        self.box_name = box_name
        
    def addUser(self, username, password):
        if self.provider == 'docker':
            return False
        self.users.append((username,password))
        return True
            
    def genUserScript(self):
        if len(self.users) == 0:
            return ''
        rtn = ''
        if self.os == 'win':
            for user in self.users:
                rtn += '$password = ConvertTo-SecureString "' + user[1] + '" -AsPlainText -Force\n'
                rtn += 'New-LocalUser "' + user[0] + '" -Password $password -Description "Added by Environment Generator"\n'
        else:
            rtn += '#!/bin/bash\n'
            for user in self.users:
                rtn += 'sudo adduser ' + user[0] + ' --gecos "Added by Environment Generator" --disabled-password\n'
                rtn += 'echo "' + user[0] + ':' + user[1] + '" | sudo chpasswd\n'
        return rtn
    
    def addSoftware(self, puppetSoftware, version=None):
        if self.provider == 'docker':
            return False
        self.software.append((puppetSoftware,version))
        return True
        
    def genManifest(self):
        if len(self.software) == 0:
            return ''
        rtn = ''
        for module in self.software:
            rtn += "module { '" + module[0] + "':\n"
            if module[1]:
                rtn += "\tensure => '" + module[1] + "',\n}\n"
            else:
                rtn += "\tensure => present,\n}\n"
        return rtn
        
    
    def toString(self):
        rtn = '\tconfig.vm.define "' + self.name + '" do |' + self.name + '|\n'
        if self.provider == 'hyperv':
            rtn += '\t\t' + self.name + '.vm.box = "' + self.box_name + '"\n'
            rtn += '\t\t# OS: "' + self.os + '"\n'
            if len(self.users) > 0:
                rtn += '\t\t' + self.name + '.vm.provision "shell", path: "users/'
                if self.os == 'win':
                    rtn += self.name + '.ps1\n'
                else:
                    rtn += self.name + '.sh\n'
            if len(self.software) > 0:
                if self.os == 'win':
                    rtn += '\t\t' + self.name + '.vm.provision "shell", path: "https://raw.githubusercontent.com/jonebeabout/envgen/master/envgen/envgen/puppet.ps1"\n'
                else:
                    rtn += '\t\t' + self.name + '.vm.provision "shell", path: "https://raw.githubusercontent.com/jonebeabout/envgen/master/envgen/envgen/puppet.sh"\n'
                rtn += '\t\t' + self.name + '.vm.provision "puppet" do |puppet|\n'
                rtn += '\t\t\tpuppet.manifest_path = "manifests"\n'
                rtn += '\t\t\tpuppet.manifest_file = "' + self.name + '.pp"\n\t\tend\n'
            if self.mem or self.cpu or self.mac:
                rtn_hyperv += '\t\t' + self.name + '.vm.provider "hyperv" do |h|\n'
                if self.mem:
                    rtn += '\t\t\th.maxmemory = ' + str(self.mem) + '\n'
                if self.cpu:
                    rtn += '\t\t\th.cpus = ' + str(self.cpu) + '\n'
                if self.mac:
                    rtn += '\t\t\th.mac = ' + mac + '\n'
                rtn += '\t\tend\n'
            else:
                rtn += '\t\t' + self.name + '.vm.provider "hyperv"\n'
        else:
            rtn += '\t\t' + self.name + '.vm.provider "docker" do |d|\n'
            rtn += '\t\t# OS: "' + self.os + '"\n'
            if len(self.dockerfile) > 0:
                rtn += '\t\t\td.build_dir = "dockerfiles/"\n'
                rtn += '\t\t\td.dockerfile = "' + self.name + '"\n'
            else:
                rtn += '\t\t\td.image = "' + self.box_name + '"\n'
            if len(self.vols) > 0:
                rtn += '\t\t\td.volumes = ['
                for vol in self.vols:
                    rtn += '"' + vol + '",'
                rtn = rtn[:-1]
                rtn += ']\n'
            if len(self.ports) > 0:
                rtn += '\t\t\td.ports = ['
                for port in self.ports:
                    rtn += '"' + port + '",'
                rtn = rtn[:-1]
                rtn += ']\n'
            rtn += '\t\t\tend\n'
            rtn += '\t\tend\n'
        rtn += '\tend\n'
        return rtn
        
class Environment:
    
    def __init__(self, name, dir, vconf=None, pconf=None, users=None, dockerfiles=None):
        self.projectName = name
        self.projectDir = dir
        if vconf:
            self.vagrantFiles = vconf
        else:
            self.vagrantFiles = []
        if pconf:
            self.puppetManifests = pconf
        else:
            self.puppetManifests = []
        if users:
            self.userFiles = users
        else:
            self.userFiles = []
        if dockerfiles:
            self.dockerfiles = dockerfiles
        else:
            self.dockerfiles = []
        self.entities = []
        if len(self.vagrantFiles) > 0:
            self.loadEnv()
        
    def loadEnv(self):
        names = re.compile('define "(.*)"')
        box = re.compile('box = "(.*)"')
        operating_system = re.compile('OS: "(.*)"')
        memory = re.compile('maxmemory = (\d+)')
        cpus = re.compile('cpus = (\d+)')
        mac = re.compile('mac = (.*)\n')
        l_users = re.compile('echo "(.*)"')
        passw = re.compile('String "(.*)"')
        w_users = re.compile('LocalUser "(.*)"')
        module = re.compile("module { '(.*)'")
        version = re.compile('ensure => (.*),')
        entities = self.vagrantFiles[0].split('\n\tend')[:-1]
        user_file = 0
        puppet_file = 0
        for e in entities:  
            n = names.findall(e)[0]
            b = box.findall(e)[0]
            os = operating_system.findall(e)[0]
            p = 'hyperv'
            if e.find('maxmemory') != -1:
                mem = int(memory.findall(e)[0])
            else:
                mem = None
            if e.find('cpu') != -1:
                c = int(cpus.findall(e)[0])
            else:
                c = None
            if e.find('mac') != -1:
                m = mac.findall(e)[0]
            else:
                m = None
            if e.find('users') != -1:
                if self.userFiles[user_file].find('#!/bin/bash') != -1:
                    us = l_users.findall(self.userFiles[user_file])
                    users = []
                    for u in us:
                        s = u.split(':')
                        users.append((s[0],s[1]))
                else:
                    us = w_users.findall(self.userFiles[user_file])
                    pw = passw.findall(self.userFiles[user_file])
                    users = zip(us,pw)
                user_file += 1
            else:
                users = None
            if e.find('puppet') != -1:
                sw = module.findall(self.puppetManifests[puppet_file])
                versions = version.findall(self.puppetManifests[puppet_file])
                vs = []
                for v in versions:
                    if v.find('present') != -1:
                        vs.append(None)
                    else:
                        vs.append(v[1:-1])
                software = zip(sw,vs)
                puppet_file += 1
            else:
                software = None
            self.entities.append(Entity(n,b,os,p,users=users, software=software, mem=mem, cpu=c, mac=m))
        if len(self.vagrantFiles) > 1:
            entities = self.vagrantFiles[1].split('\n\tend')[:-1]
            im = re.compile('image = "(.*)"')
            ports = re.compile('ports = \[(.*)\]')
            vols = re.compile('volumes = \[(.*)\]')
            docker_file = 0
            for e in entities:
                n = names.findall(e)[0]
                if e.find('image') != -1:
                    b = im.findall(e)[0]
                    d = None
                else:
                    b = 'None'
                    d = self.dockerfiles[docker_file]
                    docker_file += 1
                os = 'linux'
                p = 'docker'
                if e.find('ports') != -1:
                    pts = ports.findall(e)[0]
                    ps = pts.split(',')
                    for i in range(len(ps)):
                        ps[i] = ps[i][1:-1]
                else:
                    ps = None
                if e.find('volumes') != -1:
                    volumes = vols.findall(e)[0]
                    vs = volumes.split(',')
                    for i in range(len(vs)):
                        vs[i] = vs[i][1:-1]
                else:
                    vs = None
                self.entities.append(Entity(n,b,os,p,vols=vs, ports=ps, dockerfile=d))

    def addEntity(self,entity):
        self.entities.append(entity)
        
    def toString(self):
        rtn_hyperv = 'Vagrant.configure("2") do |config|\n'
        rtn_docker = 'Vagrant.configure("2") do |config|\n'
        for entity in self.entities:
            if entity.provider == 'hyperv':
                rtn_hyperv += entity.toString()
            else:
                rtn_docker += entity.toString()
        rtn_hyperv += 'end'
        rtn_docker += 'end'
        return (rtn_hyperv,rtn_docker)
        
class EnvironmentGenerator:

    def __init__(self):
        self.host = self.updateHost()
        self.workingEnv = None;
        self.v = vagrant.Vagrant(quiet_stdout=False)
        
    def updateHost(self):
        hname = socket.gethostname()
        mem = psutil.virtual_memory()
        dsks = [x[0] for x in psutil.disk_partitions()]
        dsk = [(x,psutil.disk_usage(x)) for x in dsks]
        cpu = (psutil.cpu_percent(),psutil.cpu_count())
        return Host(hname,mem,dsk,cpu)
        
    def loadEnv(self, name, dir):
        vconf = []
        pconf = []
        users = []
        dockerfiles = []
        try:
            projectFolder = os.listdir(dir)
        except:
            os.mkdir(dir)
            os.mkdir(dir + 'hyperv/')
            os.mkdir(dir + 'hyperv/users/')
            os.mkdir(dir + 'hyperv/manifests/')
            os.mkdir(dir + 'docker/')
            os.mkdir(dir + 'docker/dockerfiles')
            projectFolder = os.listdir(dir)
            pass
        hyperv = os.listdir(dir + 'hyperv/')
        if 'Vagrantfile' in hyperv:
            with open(dir+'hyperv/Vagrantfile','r') as file:
                vconf.append(file.read())
        if 'manifests' in hyperv:
            puppet_dir = dir+'hyperv/manifests/'
            for filename in os.listdir(puppet_dir):
                with open(puppet_dir+filename,'r') as file:
                    pconf.append(file.read())
        if 'users' in hyperv:
            user_dir = dir+'hyperv/users/'
            for filename in os.listdir(user_dir):
                with open(user_dir+filename,'r') as file:
                    users.append(file.read())
        docker = os.listdir(dir + 'docker/')
        if 'Vagrantfile' in docker:
            with open(dir+'docker/Vagrantfile','r') as file:
                vconf.append(file.read())
        if 'dockerfiles' in docker:
            docker_dir = dir+'docker/dockerfiles/'
            for filename in os.listdir(docker_dir):
                with open(docker_dir+filename,'r') as file:
                    dockerfiles.append(file.read())
        self.workingEnv = Environment(name,dir,vconf,pconf,users,dockerfiles)
        return True
        
    def checkResources(self):
        if self.workingEnv:
            error = 0
            rtn = ''
            self.host = self.updateHost()
            mem_needed = 0
            for entity in self.workingEnv.entities:
                if entity.mem:
                    mem_needed += entity.mem
                else:
                    mem_needed += 1024 # default 1GB / machine
            mem_remaining = self.host.memory[1]/1024/1024 - mem_needed
            if mem_remaining <= 0:
                error += 1
                rtn += 'There is not enough memory for this environment.\nMemory Available: '+self.host.mem[1]/1024/1024+'MB\nMemory Required: '+mem_needed+'MB\n'
            else:
                rtn += 'There is enough memory for this environment\n'
            return (error,rtn)
        return (1,'No project loaded')        
    
    def buildEntity(self, name, box_name, os, provider, mem=None, cpu=None, mac=None, vols=None, ports=None, dockerfile=None):
        if self.workingEnv:
            print vols, ports, dockerfile
            entity = Entity(name,box_name,os,provider,mem=mem,cpu=cpu,mac=mac,vols=vols,ports=ports,dockerfile=dockerfile)
            self.workingEnv.addEntity(entity)
            return True
        return False
            
    def removeEntity(self, name):
        if name in [e.name for e in self.workingEnv.entities]:
            for e in self.workingEnv.entities:
                if e.name == name:
                    self.workingEnv.entities.remove(e)
                    return True
            return False
        return False
    
    def buildConfig(self):
        if self.workingEnv:
            with open(self.workingEnv.projectDir+'hyperv/Vagrantfile','w') as file:
                file.write(self.workingEnv.toString()[0])
            with open(self.workingEnv.projectDir+'docker/Vagrantfile','w') as file:
                file.write(self.workingEnv.toString()[1])
            for entity in self.workingEnv.entities:
                if len(entity.users) > 0:
                    if entity.os == 'win':
                        with open(self.workingEnv.projectDir+'hyperv/users/'+entity.name+'.ps1','w') as file:
                            file.write(entity.genUserScript())
                    else:
                        with open(self.workingEnv.projectDir+'hyperv/users/'+entity.name+'.sh','w') as file:
                            file.write(entity.genUserScript())
                if len(entity.software) > 0:
                    with open(self.workingEnv.projectDir+'hyperv/manifests/'+entity.name+'.pp','w') as file:
                        file.write(entity.genManifest())
                if entity.dockerfile:
                    with open(self.workingEnv.projectDir+'docker/dockerfiles/'+entity.name,'w') as file:
                        file.write(entity.dockerfile)
            return True
        return False
        
    def startEnv(self):
        check = self.checkResources()
        if check[0] > 0:
            colorama.init()
            print colorama.Fore.RED + check[1] + colorama.Style.RESET_ALL
            colorama.deinit()
            return False
        else:
            print check[1]
        os_env = os.environ.copy()
        dir = self.workingEnv.projectDir + 'hyperv/'
        os_env['VAGRANT_CWD'] = dir.replace('/','\\')
        self.v.env = os_env
        self.v.up(provider='hyperv')
        dir = self.workingEnv.projectDir + 'docker/'
        os_env['VAGRANT_CWD'] = dir.replace('/','\\')
        self.v.env = os_env
        self.v.up(provider='docker')
        return True









        
