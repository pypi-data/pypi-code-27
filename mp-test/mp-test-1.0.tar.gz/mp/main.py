

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def root():
    a = request.args.get('a')
    request.get_json()
    return a



