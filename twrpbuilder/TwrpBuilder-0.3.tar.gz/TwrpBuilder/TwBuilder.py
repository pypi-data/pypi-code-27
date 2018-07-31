#!/usr/bin/env python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from tqdm import tqdm
import requests
import math
import os
from urllib import request
import json

slash='/'
myPath=os.path.dirname(os.path.realpath(__file__))+slash
Cred=credentials.Certificate(myPath+"Cert.py")
firebaseApp=firebase_admin.initialize_app(Cred,{'databaseURL':'https://twrpbuilder.firebaseio.com','storageBucket':'twrpbuilder.appspot.com'})
firebaseStorage=storage.bucket()
outDir='work'
jarFile=''
backupFile=''

def update():
    key='?client_id=8e59ef85a15407f3aaf0&client_secret=e931a914c3c3d4500e59766ffa6578e1d4318329'
    apiUrl='https://api.github.com/repos/TwrpBuilder/twrpbuilder_tree_generator/releases/latest'+key
    global jarFile
    out=request.urlopen(apiUrl)
    j=json.loads(out.read())
    dloadUrl=j['assets'][0]['browser_download_url']
    name=j['assets'][0]['name']
    size=j['assets'][0]['size']
    jarFile=name
    if not os.path.exists(name):
        downloadData(dloadUrl, name, size, workDir=False)

def build():
    ref = db.reference('RunningBuild')
    snapshot = ref.get()
    global backupFile
    for key, val in snapshot.items():
        model=val['model']
        brand=val['brand']
        board=val['board']
        codeName=val['codeName']
        date=val['date']
        email=val['email']
        developerEmail=val['developerEmail']
        path='queue/'+brand+slash+board+slash+model
        blobData=firebaseStorage.get_blob(path+"/TwrpBuilderRecoveryBackup.tar.gz")
        blobData.make_public()
        url=firebaseStorage.get_blob(path+"/TwrpBuilderRecoveryBackup.tar.gz").public_url
        print( f'Model= {model} \nCodename= {codeName} \nBoard={board} \nRequested by= {email}\nRequested on= {date}')
        backupFile = outDir+slash+model.replace(" ", "_")+ '.tar.gz'
        switchBuild(getData(url, name=model.replace(" ", "_") + '.tar.gz', size=blobData.size))

def switchBuild(case):
    if (case == 0):
        exit(-1)
    elif (case == 1):
        buildTree()
    else:
        buildTree(old=True)

def buildTree(old=False):
    print(os.system('java -jar '+jarFile+" -f "+backupFile))
    return 0

def getData(url, name='output.bin', size=0):
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    if not os.path.exists(outDir + slash + name) or size != int(os.path.getsize(outDir + slash + name)):
        if size != 0 and downloadData(url,name,size) != size:
                print("ERROR, something went wrong")
                return 0
        else:
            return 1
    else:
        print('Skipping '+name)
        return 2


def downloadData(url,name,size,workDir=True):
    r = requests.get(url, stream=True)
    block_size = 1000
    wrote = 0
    if workDir==True:
        out=outDir + "/" + name
    else:
        out=name
    with open(out, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(size // block_size), unit='Kb'):
            wrote = wrote + len(data)
            f.write(data)
    return wrote

update()