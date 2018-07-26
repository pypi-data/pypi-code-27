
import os
from flask import Flask

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)


##########register_blueprint##########
root_url = app.config['ROOT_URL']

from app.auth.views import auth
app.register_blueprint(auth, url_prefix=root_url)

from app.cluster.views import cluster
app.register_blueprint(cluster, url_prefix=root_url)

from app.node.views import node
app.register_blueprint(node, url_prefix=root_url)

from app.corosync.views import corosync
app.register_blueprint(corosync, url_prefix=root_url)
