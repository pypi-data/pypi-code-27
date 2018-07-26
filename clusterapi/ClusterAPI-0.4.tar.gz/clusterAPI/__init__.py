
import os
from flask import Flask

api = Flask(__name__)

api_settings = os.getenv(
    'APP_SETTINGS',
    'clusterAPI.config.DevelopmentConfig'
)
api.config.from_object(api_settings)


##########register_blueprint##########
root_url = api.config['ROOT_URL']

from clusterAPI.auth.views import auth
api.register_blueprint(auth, url_prefix=root_url)

from clusterAPI.cluster.views import cluster
api.register_blueprint(cluster, url_prefix=root_url)

from clusterAPI.node.views import node
api.register_blueprint(node, url_prefix=root_url)

from clusterAPI.corosync.views import corosync
api.register_blueprint(corosync, url_prefix=root_url)
