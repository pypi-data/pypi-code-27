"""
RRDS Template Library
(c) Monty Dimkpa
"""
from flask import Flask, Response, request, redirect
from flask_cors import CORS
from collections import OrderedDict
from rigo import *
from flask_restful import Resource, Api

app = Flask(__name__)
CORS(app)

global rrds_port

rrds_port = 7737

def validData(data):
    try:
        test = eval(data);
        result = False
    except:
        result = True
    return result

def message_formatter(code,message,data={}):
    if data != {}:
        msg = OrderedDict();
        msg["code"] = code;
        msg["message"] = message;
        msg["data"] = data;
        return Response(json.dumps(msg), status=code, mimetype='application/json')
    else:
        msg = OrderedDict();
        msg["code"] = code;
        msg["message"] = message;
        return Response(json.dumps(msg), status=code, mimetype='application/json')

# Execution Wrapper
def Execute(command,options={}):
    start = datetime.datetime.today()
    dbmessage = RigoDB(command,options)
    duration = (datetime.datetime.today() - start).seconds
    if command == "view_entries":
        try:
            columnar = uniform_dataset(dbmessage)
            dbmessage = columnar
        except:
            pass
        return message_formatter(200,"Query OK. [lasted: %ds]" % duration, dbmessage)
    elif command == "list_databases" or command == "list_tables":
        return message_formatter(200,"Query OK. [lasted: %ds]" % duration, dbmessage)
    elif command == "join":
        if 'dict' in str(type(dbmessage)):
            info = dbmessage["info"]
            data = dbmessage["data"]
            return message_formatter(200,"%s [lasted: %ds]" % (info,duration),data)
        else:
            return message_formatter(200,"%s [lasted: %ds]" % (dbmessage,duration))
    else:
        return message_formatter(200,"%s [lasted: %ds]" % (dbmessage,duration))


class CreateDatabase(Resource):
    def get(self):
        command = "new_database";
        options = {};
        options["dbname"] = request.args.get("dbname");
        options["dbpassword"] = request.args.get("dbpassword");
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

class AddTable(Resource):
    def get(self):
        command = "add_table";
        options = {};
        options["dbname"] = request.args.get("dbname");
        options["dbpassword"] = request.args.get("dbpassword");
        options["tablename"] = request.args.get("tablename");
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

class NewEntry(Resource):
    def post(self):
        command = "new_entry";
        options = request.get_json(force=True);
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        try:
            data = options["entry"]
            if validData(data):
                return Execute(command,options)
            else:
                return message_formatter(400,"error: please check your [entry] argument. Should be JSON")
        except:
            return message_formatter(400,"error: please check your [entry] argument. Should be JSON")

class ViewEntries(Resource):
    def get(self):
        command = "view_entries";
        options = {};
        options["dbname"] = request.args.get("dbname");
        options["dbpassword"] = request.args.get("dbpassword");
        options["tablename"] = request.args.get("tablename");
        try:
            options["entry_pos"] = eval(request.args.get("entry_pos"));
        except:
            return message_formatter(400,"error: please check your [entry_pos] argument. Should be List or *")
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

class EditEntry(Resource):
    def post(self):
        command = "edit_entry";
        options = request.get_json(force=True);
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        try:
            data = options["entry_pos"]
            data1 = options["new"]
            if validData(data) and validData(data1):
                return Execute(command,options)
            else:
                return message_formatter(400,"error: please check your [entry_pos,new] arguments. Should be [Integer,JSON] respectively")
        except:
            return message_formatter(400,"error: please check your [entry_pos,new] arguments. Should be [Integer,JSON] respectively")

class DeleteEntry(Resource):
    def get(self):
        command = "delete_entry";
        options = {};
        options["dbname"] = request.args.get("dbname");
        options["dbpassword"] = request.args.get("dbpassword");
        options["tablename"] = request.args.get("tablename");
        try:
            options["entry_pos"] = eval(request.args.get("entry_pos"));
        except:
            return message_formatter(400,"error: please check your [entry_pos] argument. Should be Integer.")
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

class DeleteTable(Resource):
    def get(self):
        command = "delete_table";
        options = {};
        options["dbname"] = request.args.get("dbname");
        options["dbpassword"] = request.args.get("dbpassword");
        options["tablename"] = request.args.get("tablename");
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

class DeleteDatabase(Resource):
    def get(self):
        command = "delete_database";
        options = {};
        options["dbname"] = request.args.get("dbname");
        options["dbpassword"] = request.args.get("dbpassword");
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

class ListDatabases(Resource):
    def get(self):
        command = "list_databases";
        options = {};
        return Execute(command,options)

class ListTables(Resource):
    def get(self):
        command = "list_tables";
        options = {};
        options["dbname"] = request.args.get("dbname");
        options["dbpassword"] = request.args.get("dbpassword");
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

class RowCount(Resource):
    def get(self):
        command = "row_count";
        options = {};
        options["dbname"] = request.args.get("dbname");
        options["dbpassword"] = request.args.get("dbpassword");
        options["tablename"] = request.args.get("tablename");
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

class LastChanged(Resource):
    def get(self):
        command = "last_changed";
        options = {};
        options["dbname"] = request.args.get("dbname");
        options["dbpassword"] = request.args.get("dbpassword");
        options["tablename"] = request.args.get("tablename");
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

class Join(Resource):
    def get(self):
        command = "join";
        options = {};
        try:
            options["join_field"] = eval(request.args.get("join_field"));
        except:
            options["join_field"] = request.args.get("join_field");
        try:
            options["targets"] = eval(request.args.get("targets"));
            options["join_values"] = eval(request.args.get("join_values"));
            options["ranged"] = eval(request.args.get("ranged"));
            options["grouped"] = eval(request.args.get("grouped"));
            options["as_table"] = eval(request.args.get("as_table"));
        except:
            return message_formatter(400,"error: please check your [targets,join_values,ranged,grouped,as_table] arguments. Should be [JSON,List,Boolean,Boolean,Boolean] respectively")
        if options["as_table"]:
            options["dbname"] = request.args.get("dbname");
            options["dbpassword"] = request.args.get("dbpassword");
            options["tablename"] = request.args.get("tablename");
        if "None" in map(str,[options[x] for x in options]):
            return message_formatter(400,"error: please provide non-null arguments")
        else:
            return Execute(command,options)

api = Api(app)

api.add_resource(CreateDatabase,'/rigo-remote/create-db')
api.add_resource(AddTable,'/rigo-remote/add-table')
api.add_resource(NewEntry,'/rigo-remote/new-entry')
api.add_resource(ViewEntries,'/rigo-remote/view-entries')
api.add_resource(EditEntry,'/rigo-remote/edit-entry')
api.add_resource(DeleteEntry,'/rigo-remote/delete-entry')
api.add_resource(DeleteTable,'/rigo-remote/delete-table')
api.add_resource(DeleteDatabase,'/rigo-remote/delete-db')
api.add_resource(ListDatabases,'/rigo-remote/list-dbs')
api.add_resource(ListTables,'/rigo-remote/list-tables')
api.add_resource(Join,'/rigo-remote/join')
api.add_resource(RowCount,'/rigo-remote/row-count')
api.add_resource(LastChanged,'/rigo-remote/last-changed')

@app.route('/')
def homepage():
    return redirect("https://www.linkedin.com/in/monty-dimkpa-82506538/",code=302)

@app.route('/rigo-remote/')
def homepage2():
    return redirect("https://www.linkedin.com/in/monty-dimkpa-82506538/",code=302)
