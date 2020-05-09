from flask import Flask, jsonify
from flask_cors import CORS

from server.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(__name__)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.route('/ping', methods=['GET'])
    def ping_pong():
        return jsonify('pong!')

    return app