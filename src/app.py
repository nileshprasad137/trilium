from flask import Flask
from flask_cors import CORS

import config_provider
import routes
from audit_api import audit_api
from migration_api import migration_api
from notes_api import notes_api
from notes_history_api import notes_history_api
from notes_move_api import notes_move_api
from password_api import password_api
from settings_api import settings_api
from sql import connect, getOption
from tree_api import tree_api

config = config_provider.getConfig()

documentPath = config['Document']['documentPath']
connect(documentPath)

flask_secret_key = getOption("flask_secret_key")

if not flask_secret_key:
    print("Application has not been setup yet. Run 'python setup.py' to finish setup.")
    exit(1)

app = Flask(__name__)
app.secret_key = flask_secret_key
app.register_blueprint(routes.routes)
app.register_blueprint(tree_api)
app.register_blueprint(notes_api)
app.register_blueprint(notes_move_api)
app.register_blueprint(password_api)
app.register_blueprint(settings_api)
app.register_blueprint(notes_history_api)
app.register_blueprint(audit_api)
app.register_blueprint(migration_api)

CORS(app)

routes.init(app)

port = config['Network']['port']
https = config['Network']['https']
certPath = config['Network']['certPath']
certKeyPath = config['Network']['certKeyPath']

if __name__ == "__main__":
    ssl_context = None

    if https == "true":
        ssl_context = (certPath, certKeyPath)

    app.run(host='0.0.0.0', port=port, ssl_context = ssl_context)