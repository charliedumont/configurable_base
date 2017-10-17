import logging
from pprint import PrettyPrinter

from google.appengine.ext import ndb

from pbi.errors import CustomException

from helpers import Helpers, UserHelpers
from helpers import app

class TestUserInterface(Helpers):

    def test_login(self):
        self._start_()
        uh = UserHelpers()
        uh.create_users()
        user_list = uh.config['testers']
        for user in user_list:
            params_for_login = {uh.key_arg: user[uh.key_arg],
                "password": user['password']}
            response = app.post_json('/api/login', params=params_for_login)
            self.assertEqual(response.status_code, 200)
        # Test with no key arg
        params_for_login = {'failing': 'failing',
            "password": ''}
        err1_response = app.post_json('/api/login', params=params_for_login, expect_errors=True)
        err1_json = err1_response.json
        self.assertEqual(err1_response.status_code, 400)
        self.assertEqual(err1_json['details'], "no {0} provided".format(uh.key_arg))
        # Test with bad password
        params_for_login = {uh.key_arg: user[uh.key_arg],
            "password": ''}
        err2_response = app.post_json('/api/login', params=params_for_login, expect_errors=True)
        err2_json = err2_response.json
        self.assertEqual(err2_response.status_code, 401)
        pp = PrettyPrinter()
        pp.pprint(err2_json)
        self.assertEqual(err2_json['details'], "Login Failed bad password")
        # Test with unknown user
        params_for_login = {uh.key_arg: 'd',
            "password": user['password']}
        err3_response = app.post_json('/api/login', params=params_for_login, expect_errors=True)
        err3_json = err3_response.json
        self.assertEqual(err3_response.status_code, 401)
        self.assertEqual(err3_json['details'], "Login Failed bad id")

    def test_create(self):
        self._start_()
        uh = UserHelpers()
        user_list = uh.config['testers']
        for user in user_list:
            response = app.post_json('/api/signup', params=user)
            self.assertEqual(response.status_code, 200)
            err_response = app.post_json('/api/signup', params=user, expect_errors=True)
            err_json = err_response.json
            self.assertEqual(err_response.status_code, 400)
            self.assertEqual(err_json['details'], "Duplicate user id")

