"""This Module is the interface of user login and signup api """
import importlib
import logging

import ndb_json

from pbi.config import Config
from pbi.data.user import UserCreator, UserValidator
from pbi.decorators import set_options, set_json
from pbi.errors import CustomException, ErrorReturn
from pbi.handlers import BaseRequestHandler
import pbi.token


class SignUp(BaseRequestHandler):
    """ Api interface handler for signup """

    @set_json
    @set_options
    def post(self):
        """ Post end point, receives json """
        params = self.req_params
        try:
            creator = UserCreator(self.user_model)
            creator.verify_args(params)
            creator.create_by_args(params)
        except CustomException as cex:
            logging.info("aborting signup with 400, user id is duplicate")
            cex.respond(status=400, response=self.response)
            return
        json_dict = {"success": True}
        self.response.write(ndb_json.dumps(json_dict))


class Login(BaseRequestHandler):
    """ API endpoint for handling login """

    @set_json
    @set_options
    def post(self):
        """ Post end point, receives json """
        params = self.req_params
        prime_key = Config.get('users', 'key_arg')
        if prime_key in params.keys():
            email = params[prime_key].lower()
        else:
            details = 'no {0} provided'.format(prime_key)
            error_msg = ErrorReturn(self.response,
                                    error_code='', details=details)
            error_msg.handle_response(status=400)
            return
        password = params['password']
        json_dict = {"success": "1"}
        try:
            usv = UserValidator(self.auth)
            user = usv.check_login(email, password)
            self._handle_other_validators(user, params)
            self._handle_other_recorders(user, params)
            token = pbi.token.generate(user)
            json_dict["jwt"] = token
        except CustomException as cex:
            logging.info("Custom exception: " + cex.details)
            cex.respond(response=self.response, status='401')
            return
        self.response.write(ndb_json.dumps(json_dict))

    @staticmethod
    def _handle_other_recorders(user, params):
        recorders = Config.get('users', 'recorders')
        plugin_dir = Config.get('general', 'plugin_dir')

        for rec in recorders:
            plug_path = plugin_dir + '.' + rec
            try:
                mod = importlib.import_module(plug_path)
            except ImportError:
                details = "Failed to load {module}".format(module=plug_path)
                raise CustomException(details=details)
            class_ = getattr(mod, 'Recorder')
            recorder = class_(user=user, params=params)
            recorder.record()


    @staticmethod
    def _handle_other_validators(user, params):
        user_validators = Config.get('users', 'validators')
        plugin_dir = Config.get('general', 'plugin_dir')

        for usv in user_validators:
            plug_path = plugin_dir + '.' + usv
            try:
                mod = importlib.import_module(plug_path)
            except ImportError:
                details = "Failed to load {module}".format(module=plug_path)
                raise CustomException(details=details)
            class_ = getattr(mod, 'Validator')
            validator = class_(user=user, params=params)
            validator.validate()
