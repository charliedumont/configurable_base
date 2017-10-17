import jwt
import logging
from pprint import PrettyPrinter

from datetime import datetime, timedelta

from pbi.config import Config


def extract(headers):
    token = None
    if 'Authorization' in headers:
        # Strip off "Token:"
        token = headers['Authorization'][6:]
    if not token:
        return None
    try:
        data = jwt.decode(token,
                          Config.get('main', 'jwt_secret'),
                          algorithms=['HS256'])
        # Expiration
        expires = datetime.utcfromtimestamp(int(data['expires']))
        if expires <= datetime.utcnow():
            return False
        return data
    except jwt.exceptions.InvalidTokenError:
        logging.info("invalid token error")
        return False


def generate(user):
    expires = datetime.utcnow() + timedelta(days=3)
    token = jwt.encode(
        {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "user_type": user.userType,
            "expires": expires.strftime("%s"),
        },
        Config.get('main', 'jwt_secret'),
        algorithm='HS256'
    )
    return token


