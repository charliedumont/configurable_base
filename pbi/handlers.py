""" Our core rendering pieces """
# Pylint doesn't want to look into the right dirs even w/ pythonpath updated
import webapp2 #pylint: disable=import-error
from webapp2_extras import auth#pylint: disable=import-error

from models import User

import pbi.token

class BaseRequestHandler(webapp2.RequestHandler):
    """ Our default handler """

    def dispatch(self):
        """ This is the basic dispatch for all requests """
        webapp2.RequestHandler.dispatch(self)

    # to handle all of the routing args
    def options(self, *args, **kwargs): #pylint: disable=unused-argument
        """ Try to set CORS headers for all subclass
        doesn't seem to work """
        headers = self.response.headers
        headers['Access-Control-Allow-Origin'] = '*'
        headers['Access-Control-Allow-Headers'] = \
            'Origin, X-Requested-With, Content-Type, Accept, Key, Authorization '
        headers['Access-Control-Allow-Credentials'] = 'true'
        headers['Access-Control-Expose-Headers'] = '*'
        headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT'

    @webapp2.cached_property
    def auth(self):#pylint: disable=no-self-use
        """ Simple method to access webapp2's auth predictably"""
        return auth.get_auth()

    @webapp2.cached_property
    def user_model(self):
        """returns the implementation of the user model.
        it is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """
        return self.auth.store.user_model#pylint: disable=no-member

    @webapp2.cached_property
    def current_user(self):
        """Returns currently logged in user"""
        user_info = pbi.token.extract(self.request.headers)
        user = User.get_by_id(user_info["user_id"])
        return user
