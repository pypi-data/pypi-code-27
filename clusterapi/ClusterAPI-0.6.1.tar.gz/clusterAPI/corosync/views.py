from flask import Blueprint, send_from_directory, request
from flask.views import MethodView
from clusterAPI.auth.helper import token_required

corosync = Blueprint('corosync', __name__)


class CorosyncConf(MethodView):
    #@token_required
    def get(self, corosync_file):
        """
        Get file from /etc/corosync
        ---
        parameters:
          - corosync_file: file from /etc/corosync
        responses:
          200:        
            description: get specific file
        """
        return send_from_directory("/etc/corosync", corosync_file)

    #@token_required
    def post(self, corosync_file):
        """
        Post file to /etc/corosync
        ---
        parameters:
          - corosync_file: file from /etc/corosync
        responses:
          200:        
            description: post specific file
        """
        file = request.files['file']
        if file.filename == "corosync.conf":
            file.save("/etc/corosync/corosync.conf")
        return ''


conf_view = CorosyncConf.as_view('corosync')
corosync.add_url_rule('/corosync/<corosync_file>', view_func=conf_view)
