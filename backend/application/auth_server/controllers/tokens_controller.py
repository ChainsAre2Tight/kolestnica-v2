"""Provides endpoints for token management"""

from flask import Response, jsonify, make_response

from utils.my_dataclasses import Token
from utils.http_wrappers import require_refresh_token, handle_http_exceptions
from utils.exc import DeprecatedRefreshToken

# chain app and encryptor imports to register all endpoints
from auth_server.controllers.sessions_controller import app, json_encryptor

from auth_server.controllers.interfaces import TokenControllerInterface
from auth_server.services.sessions.reader import SessionReader
from auth_server.services.tokens.creator import TokenPairCreator
from auth_server.helpers.request_helpers import provide_access_token, provide_refresh_token


class TokenController(TokenControllerInterface):

    @staticmethod
    @app.route('/api/auth/refresh-tokens', methods=['POST'])
    @require_refresh_token
    @handle_http_exceptions
    @json_encryptor.encrypt_json()
    def refresh_tokens(raw_token: str, refresh_token: Token) -> tuple[Response, int]:
        # find session by refresh token
        session = SessionReader.read(browser_fingerprint=refresh_token.sessionId)

        if session.refresh_token != raw_token:  # verify raw token is the latest for this session
            raise DeprecatedRefreshToken('Provided refresh token does not match any records')

        new_token_pair = TokenPairCreator.create(browser_fingerprint=session.uuid)

        # construct response
        response_data = provide_access_token(
            {'Status': 'Refreshed tokens', 'data': {}},
            token_pair=new_token_pair
        )
        response = provide_refresh_token(
            response=make_response(jsonify(response_data)),
            token_pair=new_token_pair
        )
        return response, 200
