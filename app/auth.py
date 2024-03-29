import json
from os import environ as env

from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

ALGORITHMS = ['RS256']

''' AuthError Exception

    Custom exception class for handling authentication errors.

    Attributes:
        error (dict): A dictionary containing error details.
        status_code (int): HTTP status code associated with the error.
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


''' Method get_token_auth_header()
    Obtains the Access Token from the Authorization Header.

    Raises:
        AuthError:
        1. If no Authorization header is present.
        2. If the Authorization header is malformed.

    Returns:
        token (str): The token part of the Authorization header.
'''


def get_token_auth_header():
    """
        Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


''' Method check_permissions(permission, payload)
    Validates whether a given permission is present in the decoded JWT payload.

    Args:
        permission (str): The string representation of the desired permission (e.g., 'post:drink').
        payload (dict): The decoded JWT payload containing user information.

    Raises:
        AuthError: If permissions are not included in the payload or if the requested
                   permission string is not found in the payload permissions array.

    Returns:
        bool: True if the permission is found in the payload permissions array.
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


''' Method verify_decode_jwt(token)
    Verifies and decodes a JSON Web Token (JWT) using Auth0's JSON Web Key Set (JWKS).

    Args:
        token (str): A JSON Web Token string.

    Returns:
        payload (dict): The decoded payload from the token.

    Raises:
        AuthError: If the token is invalid, expired, or contains incorrect claims.
                   Also raised if there's an issue parsing the authentication token.
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(
        f'https://{env.get("AUTH0_DOMAIN")}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=env.get("AUTH0_AUDIENCE"),
                issuer='https://' + env.get("AUTH0_DOMAIN") + '/'
            )
            return payload

        except jwt.ExpiredSignatureError as e:
            print('Expired token', e)
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError as e:
            print('Claim fail', e)
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception as e:
            print('Generic error', str(e))
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


''' Decorator requires_auth(permission)
    Decorator to enforce authentication and authorization for API endpoints.

    Args:
        permission (str): The required permission for the endpoint (i.e., 'post:drink').

    Returns:
        requires_auth_decorator (function): A decorator function that passes the decoded payload to the decorated method.

    Raises:
        AuthError: If authentication or authorization fails, it raises an AuthError with the appropriate status code.
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except BaseException:
                abort(401)
            try:
                check_permissions(permission, payload)
            except Exception as e:
                abort(e.status_code)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
