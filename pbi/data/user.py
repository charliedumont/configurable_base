import logging
from pprint import PrettyPrinter

from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from models import User
from pbi.config import Config
from pbi.errors import CustomException, ErrorReturn


class UserCreator(object):

    def __init__(self, user_model):
        self.user_model = user_model
        self.signup_args = Config.get('users', 'signup_args')
        self.prime_key =  Config.get('users', 'key_arg')

    def verify(self, params):
        for key in self.signup_args:
            if key not in params.keys():
                details = "we don't have %s key" % key
                logging.info(details)
                raise CustomException(details=details, error_code='')

        try:
            user_type = params.get('userType')
            user_types = Config.get('users', 'user_types')
            if user_type not in user_types:
                details = "user type: %s is not supported" % params['userType']
                logging.info(details)
                raise CustomException(details=details, error_code='')
        except KeyError as e:
            details = "User types undefined, moving on"
            logging.info(details)
        return True

    def create(self, params):
        signup_args = {}
        for ar in self.signup_args:
            signup_args[ar] = params.get(ar)

        del(signup_args['password'])
        signup_args['password_raw'] = params.get('password')
        prime_key = params[self.prime_key].lower()
        unique_properties = [self.prime_key]
        user_data = self.user_model.create_user(
            prime_key,
            unique_properties,
            **signup_args
            )

        if not user_data[0]:  # user_data is a tuple
            details = "Duplicate user id"
            raise CustomException(error_code='',  details=details)
        user = user_data[1]
        user.put()
        return user


class UserValidator(object):

    def __init__(self, auth):
        self.auth = auth

    def _check_login(self, email, password):
        try:
            u = self.auth.get_user_by_password(email, password)
            user = User.get_by_id(u['user_id'])
        except InvalidAuthIdError as e:
            details = 'Login Failed bad id'
            logging.info(details)
            raise CustomException(error_code='', details=details)
        except InvalidPasswordError as e:
            details = 'Login Failed bad password'
            logging.info(details)
            raise CustomException(error_code='', details=details)
        return user


class UserFormatter(object):

    def __init__(self):
        signup_args = Config.get('users', 'signup_args')
        pp = PrettyPrinter()
        pp.pprint(signup_args)
        self.signup_args = [x for x in signup_args if x != 'password']
        pp.pprint(self.signup_args)

    def user_to_dict(self, user):
        u = user._to_dict()
        response_dict = {}
        for ar in self.signup_args:
            response_dict[ar] = u.get(ar)
        response_dict['user_id'] = user.get_id()
        response_dict['user_key'] = user.key.urlsafe()
        return response_dict



