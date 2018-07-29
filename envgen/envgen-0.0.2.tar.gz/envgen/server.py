from envgen import EnvironmentGenerator
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal
from json import dumps
import os
import shutil
import threading
import argparse

app = Flask(__name__)
api = Api(app)
e = EnvironmentGenerator()
project_dir = ''

host_fields = {
    'hostname': fields.String,
    'memory': fields.List(fields.String),
    'disks': fields.List(fields.List(fields.String)),
    'cpu_utilization': fields.String,
    'cpu_cores': fields.Integer
}

entity_fields = {
    'name': fields.String,
    'os': fields.String,
    'box_name': fields.String,
    'provider': fields.String,
    'max_memory': fields.Integer,
    'cpu_cores': fields.Integer,
    'mac_address': fields.String,
    'users': fields.List(fields.List(fields.String)),
    'software': fields.List(fields.List(fields.String)),
    'volumes': fields.List(fields.String),
    'ports': fields.List(fields.String),
    'dockerfile': fields.String
}

check_fields = {
    'errors': fields.Integer,
    'output': fields.String
}
    

class Projects(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('project', type=str, required=True, help='No project name provided', location='json')
        super(Projects, self).__init__()
    
    def get(self):
        return {'projects': os.listdir(project_dir)}
        
    def post(self):
        args = self.reqparse.parse_args()
        e.loadEnv(args['project'],project_dir+args['project']+'/')
        return {'active_project': args['project']}, 201
        
class Project_Operations(Resource):
    def put(self,arg):
        if e.workingEnv is None:
            abort(404)
        if arg == 'check':
            results = e.checkResources()
            check = {
                'errors': results[0],
                'output': results[1]
            }
            return {'resource_check': marshal(check,check_fields)}
        if arg == 'build':
            results = e.buildConfig()
            if not results:
                abort(404)
            return {'environment_built': results}
        if arg == 'start':
            thr = threading.Thread(target=e.startEnv(), args=(), kwargs={})
            thr.start()
            if not thr.is_alive():
                abort(404)
            return {'environment_started': 'Started! Please wait...'}
    
class Delete_Project(Resource):
    def delete(self,name):
        if name not in os.listdir(project_dir):
            abort(404)
        shutil.rmtree(project_dir+name)
        return {'result': True}
        
class Host(Resource):
    def get(self):
        e.updateHost()
        host = {
            'hostname': e.host.hostname,
            'memory': list(e.host.memory),
            'disks': [list(x) for x in e.host.disk],
            'cpu_utilization': (str(e.host.cpu[0]) + '%'),
            'cpu_cores': e.host.cpu[1]
        }
        return {'host': marshal(host, host_fields)}

class Entities(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='No entity name provided', location='json')
        self.reqparse.add_argument('os', type=str, required=True, help='No OS defined for entity', location='json')
        self.reqparse.add_argument('box_name', type=str, required=True, help='No box or container name defined, if dockerfile is defined please leave as "None"', location='json')
        self.reqparse.add_argument('provider', type=str, required=True, help='Provider must be "hyperv" or "docker"', location='json')
        self.reqparse.add_argument('max_memory', type=int, default=None, location='json')
        self.reqparse.add_argument('cpu_cores', type=int, default=None, location='json')
        self.reqparse.add_argument('mac_address', type=str, default=None, location='json')
        self.reqparse.add_argument('users', type=list, default=None, location='json')
        self.reqparse.add_argument('software', type=list, default=None, location='json')
        self.reqparse.add_argument('volumes', type=list, default=None, location='json')
        self.reqparse.add_argument('ports', type=list, default=None, location='json')
        self.reqparse.add_argument('dockerfile', type=str, default=None, location='json')
        super(Entities, self).__init__()
    
    def get(self):
        entities = []
        for ent in e.workingEnv.entities:
            tmp = {
                'name': ent.name,
                'os': ent.os,
                'box_name': ent.box_name,
                'provider': ent.provider
            }
            if ent.mem:
                tmp['max_memory'] = ent.mem
            if ent.cpu:
                tmp['cpu_cores'] = ent.cpu
            if ent.mac:
                tmp['mac_address'] = ent.mac
            if len(ent.users) > 0:
                tmp['users'] = [list(x) for x in ent.users]
            if len(ent.software) > 0:
                tmp['software'] = [list(x) for x in ent.software]
            if len(ent.vols) > 0:
                tmp['volumes'] = ent.vols
            if len(ent.ports) > 0:
                tmp['ports'] = ent.ports
            if ent.dockerfile != '':
                tmp['dockerfile'] = ent.dockerfile
            entities.append(tmp)
        return {'entities': [marshal(entity,entity_fields) for entity in entities]}
        
    def post(self):
        args = self.reqparse.parse_args()
        result = e.buildEntity(args['name'],args['box_name'],args['os'],args['provider'],
            mem=args['max_memory'],cpu=args['cpu_cores'],mac=args['mac_address'],
            vols=args['volumes'],ports=args['ports'],dockerfile=args['dockerfile'])
        return {'result': result}, 201
    
class Delete_Entity(Resource):
    def delete(self,name):
        result = e.removeEntity(name)
        if not result:
            abort(404)
        return {'result': result}
        
api.add_resource(Projects, '/projects')
api.add_resource(Project_Operations, '/projects/<arg>')
api.add_resource(Delete_Project, '/projects/del/<name>')
api.add_resource(Host, '/host')
api.add_resource(Entities, '/entities')
api.add_resource(Delete_Entity, '/entities/del/<name>')

def main():
    parser = argparse.ArgumentParser(description='Runs the API Server for the Environment Generator')
    parser.add_argument('project_dir', metavar='Project_Directory', help='Define the project directory.  End with forward slash(/).\nExample: C:/envgen/projects/')
    parser.add_argument('-p','--port', default=2013, type=int, help='Define the port for the server to run on')
    args = parser.parse_args()
    global project_dir
    project_dir = args.project_dir
    app.run(port=args.port)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs the API Server for the Environment Generator')
    parser.add_argument('project_dir', metavar='Project_Directory', help='Define the project directory.  End with forward slash(/).\nExample: C:/envgen/projects/')
    parser.add_argument('-p','--port', default=2013, type=int, help='Define the port for the server to run on')
    args = parser.parse_args()
    project_dir = args.project_dir
    app.run(port=args.port)