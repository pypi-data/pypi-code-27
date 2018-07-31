import os
from flask import Flask
from flask import request
import requests
import sys
reload(sys)
import logging

sys.setdefaultencoding('utf-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', encoding='utf-8')

app = Flask(__name__)
app.debug = True

@app.route('/')
def so():
    r = requests.get("http://so.com")
    return r.text

def fun():
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 6001))
    app.run(host='0.0.0.0', port=port)

def main():
	pass
	
if __name__ == '__main__':
	main()
