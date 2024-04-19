"""Provides controller that sends public key to client"""


from flask import Response, jsonify

from auth_server import app, public_key
from auth_server.controllers.interfaces import KeyControllerInterface


class KeyController(KeyControllerInterface):

    @staticmethod
    @app.route('/api/keys/public', methods=['GET'])
    def show_public_key() -> tuple[Response, int]:
        return jsonify({'public_key': public_key}), 200
