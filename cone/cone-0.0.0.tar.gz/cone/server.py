import uuid
from threading import Thread
from flask import Flask, request, jsonify
import logging

app = Flask('cone')

app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

tasks = []
results = {}

@app.route("/")
def index():
    return "cone server is running..."

@app.route('/task', methods=['GET', 'POST'])
def task():
    if request.method == 'GET':
        if len(tasks) == 0:
            return jsonify({})

        else:
            data = tasks.pop(0)
            return jsonify(data)

    else:
        content = request.get_json()
        id = uuid.uuid4()
        content['id'] = id
        tasks.append(content)
        return jsonify({'id' : id})

@app.route("/results/<string:id>", methods=['GET', 'POST'])
def result(id):
    content = request.get_json()
    if request.method == 'GET':
        data = results.pop(id, None)
        if data is not None:
            return jsonify(data)
        else:
            return jsonify(None)

    elif request.method == 'POST':
        results[id] = content
        return jsonify({})



class ServerThread(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)

    def run(self):
        app.run()


def init():
    app = ServerThread()
    app.daemon = True
    app.start()

def get_url():
    return 'http://localhost:5000'
