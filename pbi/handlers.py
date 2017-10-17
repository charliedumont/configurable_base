import logging

import webapp2
from webapp2_extras import auth

from models import User

from pbi.util import set_cors_headers
import pbi.token

class BaseRequestHandler(webapp2.RequestHandler):
    def dispatch(self):
        webapp2.RequestHandler.dispatch(self)

    def options(self):
        set_cors_headers(self.response.headers)

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    """returns the implementation of the user model.
       it is consistent with config['webapp2_extras.auth']['user_model'], if set.
    """
    @webapp2.cached_property
    def user_model(self):
        return self.auth.store.user_model

    @webapp2.cached_property
    def current_user(self):
        """Returns currently logged in user"""
        user_info = pbi.token.extract(self.request.headers)
        user = User.get_by_id(user_info["user_id"])
        return user



