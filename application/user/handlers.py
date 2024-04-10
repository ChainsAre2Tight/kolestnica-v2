from flask import request, Response, make_response, jsonify

from user.app import app
from utils.wrappers import require_access_token, handle_user_rights
import utils.my_dataclasses as dataclass
import user.queries as q
import utils.my_exceptions as exc

@app.route('/api/auth', methods=['GET'])
@require_access_token
def ping(_) -> tuple[Response, int]:
    """This endpoint provides a way to check service avaliability"""

    return jsonify('pinged'), 200

@app.route('/api/auth/register', methods=['POST'])
def register_user() -> tuple[Response, int]:
    data = request.get_json()

    try:
        _ = q.create_user(
            data['username'],
            data['login'],
            data['pdwh']
        )

        return jsonify({'Status': 'OK'}), 201

    except KeyError:
        return jsonify({'Error': 'Missing data'}), 400
    except exc.DuplicateLoginException:
        return jsonify({'Error': 'An account assosiated with this login already exists'}), 409
    except exc.DuplicateUsernameException:
        return jsonify({'Error': 'This username was already taken by another user'}), 406
