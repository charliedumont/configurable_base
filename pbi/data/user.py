""" User data accessobjects """
import logging

#pylint: disable=import-error
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from models import User
from pbi.config import Config
from pbi.errors import CustomException

class UserCreator(object):
    """ User creator control """

    def __init__(self, user_model):
        self.user_model = user_model
        self.signup_args = Config.get('users', 'signup_args')
        self.prime_key = Config.get('users', 'key_arg')

    def verify_args(self, params):
        """ Method to check incoming args against config
        and return smart error """
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
        except KeyError as kex:
            details = "User types undefined, moving on %s" % kex
            logging.info(details)
        return True

    def create_by_args(self, params):
        """ Create user based on params args """
        signup_args = {}
        for arg in self.signup_args:
            signup_args[arg] = params.get(arg)

        # we don't use password, we use the magic raw_password
        del signup_args['password']
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
            raise CustomException(error_code='', details=details)
        user = user_data[1]
        user.put()
        return user


class UserValidator(object): #pylint: disable=too-few-public-methods
    """ Class for verifying our user """

    def __init__(self, auth):
        self.auth = auth

    def check_login(self, email, password):
        """ Verify user with id and password """
        try:
            uob = self.auth.get_user_by_password(email, password)
            user = User.get_by_id(uob['user_id'])
        except InvalidAuthIdError:
            details = 'Login Failed bad id'
            logging.info(details)
            raise CustomException(error_code='', details=details)
        except InvalidPasswordError:
            details = 'Login Failed bad password'
            logging.info(details)
            raise CustomException(error_code='', details=details)
        return user


class UserFormatter(object):#pylint: disable=too-few-public-methods
    """ User formatting tools """

    def __init__(self):
        signup_args = Config.get('users', 'signup_args')
        self.signup_args = [x for x in signup_args if x != 'password']

    def user_to_dict(self, user):
        """ Helper method for returning useful parts of the User object """
        udd = user._to_dict() #pylint: disable=protected-access
        response_dict = {}
        for arg in self.signup_args:
            response_dict[arg] = udd.get(arg)
        response_dict['user_id'] = user.get_id()
        response_dict['user_key'] = user.key.urlsafe()
        return response_dict
