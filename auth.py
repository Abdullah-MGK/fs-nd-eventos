import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# https://fsnd-eventos.us.auth0.com/authorize?audience=Eventos&response_type=token&client_id=yE1MY2oQLRaBdPrAlau0C3wKvmMI9m9D&redirect_uri=http://127.0.0.1:5000/
# manager1@ev.com : manager1@ev.com : manager
# part1@ev.com : part1@ev.com : participant
# admin1@ev.com : admin1@ev.com : admin

AUTH0_DOMAIN = os.environ.get(
    'AUTH0_DOMAIN', "AUTH0_DOMAIN not found in environment")
ALGORITHMS = os.environ.get(
    'ALGORITHMS', "ALGORITHMS not found in environment")
API_AUDIENCE = os.environ.get(
    'API_AUDIENCE', "API_AUDIENCE not found in environment")


# AuthError Exception


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

# get_token_auth_header() method
def get_token_auth_header():
    # checkes if 'Authorization' exists in request
    if 'Authorization' not in request.headers:
        raise AuthError('No Authorization In Headers!', 401)

    # gets the header from the request
    auth_header = request.headers['Authorization']
    auth_header_parts = auth_header.split(' ')

    # checkes if Authorization has 2 parts only
    if len(auth_header_parts) != 2:
        raise AuthError('Invalid Authorization Header!', 401)

    # checkes if Authorization is a bearer token
    if auth_header_parts[0].lower() != 'bearer':
        raise AuthError('Not A Bearer Token!', 401)

    # returns the token part of the header
    token = auth_header_parts[1]
    return token


# check_permissions(permission, payload) method


def check_permissions(permission, payload):
    # checks if 'permissions' is included in the payload
    if 'permissions' not in payload:
        raise AuthError('No Permissions In Token!', 401)

    # checks if the required permission is in the payload permissions
    if permission not in payload['permissions']:
        raise AuthError('No Permission Found!', 401)

    # returns true if success
    return True


# verify_decode_jwt(token) method


def verify_decode_jwt(token):
    # gets the public key from Auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # gets data from token
    unverified_header = jwt.get_unverified_header(token)

    # choose RSA key
    rsa_key = {}

    # checks if token has 'kid'
    if 'kid' not in unverified_header:
        raise AuthError('No Kid In Headers!', 401)

    # assigns rsa_key to token[kid]
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if not rsa_key:
        raise AuthError("No RSA Key!", 401)

    # verifies token
    if rsa_key:
        # returns the payload if success
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError("Expired Token!", 401)

        except jwt.JWTClaimsError:
            raise AuthError("Invalid Claims", 401)

        except Exception:
            raise AuthError("Invalid Token!", 401)


# @requires_auth(permission) decorator method


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
