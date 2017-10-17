import logging
from pprint import PrettyPrinter
import unittest

from google.appengine.ext import ndb
from webtest import TestApp

import main
from models import User
from pbi.config import Config
from pbi.user import UserCreator

app = TestApp(main.app)


class Helpers(unittest.TestCase):

    def _init_(self):
        logging.info("helpers init called")

    def _start_(self):
        self.testbed.init_blobstore_stub()
        self.testbed.init_files_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_app_identity_stub()
        self.testbed.init_urlfetch_stub()


class UserHelpers(object):

    def __init__(self):
        self.user_model = User
        self.config = Config.get('users', 'testing')
        self.key_arg = Config.get('users', 'key_arg')
        self.user_list = []


    def create_users(self):
        uc = UserCreator(self.user_model)
        user_list = self.config['testers']
        tmp = {}
        for user in user_list:
            u = uc.create(user)
            tmp[u.key.urlsafe()] = u

    def login_user(self, username=None, password=None):
        params_for_login = {"email": username, "password": password}
        response = app.post_json('/api/login', params=params_for_login)
        json_dict = response.json
        self._token = json_dict["jwt"]
        token = "Token " + str(self._token)
        self._headers = {"Authorization": token}
        return response

