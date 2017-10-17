import logging
import webapp2
from webapp2_extras import json

import pbi.token
from pbi.errors import ErrorReturn

# ToDo: make this set params from json or post
def set_json(handler):
    def _json(self, *args, **kwargs):
        if self.request.method == 'POST':
            try:
                self.req_params = json.decode(self.request.body)
            except ValueError as e:
                logging.info(str(e))
                error_msg = ErrorReturn(self.response, error_code='')
                error_msg.handle_400()
                return
        elif self.request.method == 'GET':
            try:
                self.req_params = self.request.GET.mixed()
            except Exception as e:
                logging.info(str(e))
                error_msg = ErrorReturn(self.response, error_code='')
                error_msg.handle_400()
                return
        elif self.request.method == 'PUT':
            try:
                self.req_params = json.decode(self.request.body)
            except ValueError as e:
                logging.info(str(e))
                self.req_params = {}
                return
        self.response.headers['content-type'] = "application/json"
        return handler(self, *args, **kwargs)
    return _json


def set_options(handler):
    def _options(self, *args, **kwargs):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*");
        return handler(self, *args, **kwargs)
    return _options

# More useful user_required decorator, this takes user_type
# Due to the new support additional user_level is being
# scoped for protection of more nuanced support
def user_required(user_type=None, user_level=None):
    def user_req(handler):
        def check_login(self, *args, **kwargs):
            # This is highly irregular, but it allows us
            # to use our internal error handler and our
            # decorators w/o playing package games
            from pbi.errors import ErrorReturn
            token_result = pbi.token.extract(self.request.headers)
            logging.info(token_result)
            if token_result is False:
                details = "token is invalid"
                error_msg = ErrorReturn(self.response, details=details)
                error_msg.handle_401()
                return
            elif not token_result:
                details = "token is not present"
                error_msg = ErrorReturn(self.response, error_code='', details=details)
                error_msg.handle_401()
                return
            user = self.current_user
            if user_type is not None and not user.userType == user_type:
                details = "user type does not match"
                error_msg = ErrorReturn(self.response, error_code='', details=details)
                error_msg.handle_401()
                return
            else:
                return handler(self, *args, **kwargs)
        return check_login
    return user_req


