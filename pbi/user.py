import logging
from pprint import PrettyPrinter

from google.appengine.ext import ndb
from webapp2_extras import json

from pbi.config import Config
from pbi.data.user import UserCreator, UserValidator
from pbi.decorators import set_options, set_json
from pbi.errors import CustomException, ErrorReturn
from pbi.handlers import BaseRequestHandler
import pbi.token
from pbi.util import set_cors_headers


class SignUp(BaseRequestHandler):

    def options(self):
        set_cors_headers(self.response.headers)

    @set_json
    def post(self):
        params = self.req_params
        try:
            creator = UserCreator(self.user_model)
            creator.verify(params)
            creator.create(params)
        except CustomException, e:
            logging.info("aborting signup with 400, user id is duplicate")
            e.respond(status=400, response=self.response)
            return
        json_dict = {"success": True}
        self.response.write(json.encode(json_dict))


class Login(BaseRequestHandler):

    def options(self):
        set_cors_headers(self.response.headers)

    @set_json
    @set_options
    def post(self):
        params = self.req_params
        logging.info(params)
        prime_key =  Config.get('users', 'key_arg')
        if prime_key in params.keys():
            email = params[prime_key].lower()
        else:
            details='no {0} provided'.format(prime_key)
            error_msg = ErrorReturn( self.response,
                error_code='', details=details)
            error_msg.handle_400()
            return
        password = params['password']
        json_dict = { "success": "1" }
        try:
            uv = UserValidator(self.auth)
            user = uv._check_login(email, password)
            token = pbi.token.generate(user)
            json_dict["jwt"]  = token
        except CustomException as e:
            details = str(e)
            logging.info("Custom exception: " + details)
            e.respond(self.response, status='401')
            """
            error_msg = ErrorReturn(self.response, error_code='', details=details)
            error_msg.handle_401()
            """
            return
        self.response.write(json.encode(json_dict))



