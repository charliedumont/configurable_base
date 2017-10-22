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
from pbi.util import set_cors_headers


class SignUp(BaseRequestHandler):
    """ Api interface handler for signup """

    def options(self):
        set_cors_headers(self.response.headers)

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

    def options(self):
        set_cors_headers(self.response.headers)

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
            token = pbi.token.generate(user)
            json_dict["jwt"] = token
        except CustomException as cex:
            logging.info("Custom exception: " + cex.details)
            cex.respond(response=self.response, status='401')
            return
        self.response.write(ndb_json.dumps(json_dict))

    def _handle_other_validators(self, user, params):
        user_validators = Config.get('users', 'validators')
        plugin_dir = Config.get('general', 'plugin_dir')

        for usv in user_validators:
            plug_path = plugin_dir + '.' + usv
            try:
                importlib.import_module(plug_path)
            except ImportError:
                details = "Failed to load {module}".format(module=plug_path)
                raise CustomException(details=details)
            class_ = getattr(usv, 'validator')
            validator = class_(user=user, params=params)
            validator.validate()
