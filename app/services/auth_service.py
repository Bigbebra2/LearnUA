import jwt
from ..extensions import jwt_redis_blocklist
from datetime import timedelta


def logout_cookies():
    from flask import current_app, request

    access_token = request.cookies.get('access_token_cookie')
    refresh_token = request.cookies.get('refresh_token_cookie')

    token_revoked = []
    errors = []
    secret_key = current_app.config.get('JWT_SECRET_KEY')

    if access_token:
        try:
            decoded = jwt.decode(access_token, secret_key, algorithms=['HS256'])
            jti = decoded["jti"]
            jwt_redis_blocklist.set(jti, "", ex=timedelta(minutes=1))
            token_revoked.append('access_token')
        except Exception as e:
            errors.append({'access_token_error': str(e)})

    if refresh_token:
        try:
            decoded = jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
            jti = decoded['jti']
            jwt_redis_blocklist.set(jti, "", ex=timedelta(days=7))
            token_revoked.append('refresh_token')
        except Exception as e:
            errors.append({'refresh_token_error': str(e)})

    return {'errors': errors, 'revoked_tokens': token_revoked}
