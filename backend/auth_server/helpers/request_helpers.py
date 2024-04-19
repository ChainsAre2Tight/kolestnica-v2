"""This module provides helpe funtion for user handlers"""

from flask import Response

import libraries.utils.my_dataclasses as dataclass

def provide_access_token(response_data: dict, token_pair: dataclass.SignedTokenPair) -> dict:
    """`Writes` access and expiry fields into data field of provided response dictionary

    :params dict response_data: dictionary containing necessary response data
    :params SignedTokenPair token_pair: signed token pair dataclass
    :returns: modified response_data dictionary
    """
    if 'data' not in response_data.keys():
        response_data['data'] = {}

    response_data['data']['tokens'] = {'access': {}}
    response_data['data']['tokens']['access']['value'] = token_pair.access
    response_data['data']['tokens']['access']['expiry'] = token_pair.access_expiry

    return response_data

def provide_refresh_token(response: Response, token_pair: dataclass.SignedTokenPair) -> Response:
    """`Adds` a refresh token cookie to response

    :params Response response: Flask Response object
    :params SignedTokenPair token_pair: signed token pair dataclass
    :returns: modified Response object
    """

    response.set_cookie(
            key='r',
            value=token_pair.refresh,
            httponly=True,
            path='/api/tokens',
            expires=token_pair.refresh_expiry
        )

    return response
