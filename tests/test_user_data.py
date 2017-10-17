import logging
from pprint import PrettyPrinter

from pbi.data.user import UserCreator, UserValidator, UserFormatter
from pbi.errors import CustomException

from helpers import Helpers, UserHelpers


class TestUserCreator(Helpers):

    def test_verify(self):
        self._start_()
        uh = UserHelpers()
        uc = UserCreator(uh.user_model)
        user_list = uh.config['testers']
        keys_to_remove = uh.config['keys_to_remove']
        for user in user_list:
            self.assertTrue(uc.verify_args(user))
            for ktr in keys_to_remove:
                err_msg = "we don't have {0} key".format(ktr)
                tmp_value = user.pop(ktr)
                with self.assertRaises(CustomException) as cm:
                    uc.verify_args(user)
                ce = cm.exception
                self.assertEqual(ce.details, err_msg)
                user[ktr] = tmp_value

    def test_create(self):
        self._start_()
        uh = UserHelpers()
        uc = UserCreator(uh.user_model)
        user_list = uh.config['testers']
        keys_to_check = uh.config['keys_to_remove']
        for user in user_list:
            u = uc.create_by_args(user)
            for ktc in keys_to_check:
                self.assertEqual(user[ktc], getattr(u, ktc))
            with self.assertRaises(CustomException) as cm:
                u = uc.create_by_args(user)
            ce = cm.exception
            err_msg = "Duplicate user id"
            self.assertEqual(ce.details, err_msg)


class TestUserValidator(Helpers):

    """
        can't figure out how to get this the webapp2_extras.auth piece
        to load for testing here. keep generating this error
            assert getattr(_local, 'request', None) is not None, _get_request_error
        AssertionError: Request global variable is not set.
    """
    """
    def test_check_login(self):
        self._start_()
        uh = UserHelpers()
        uv = UserValidator()
        user_list = uh.config['testers']
        key = uh.key_arg
        for user in user_list:
            u = uv._check_login(user[key], user['password'])
    """

class TestUserHelper(Helpers):

    def test_user_to_dict(self):
        self._start_()
        uh = UserHelpers()
        uc = UserCreator(uh.user_model)
        uf = UserFormatter()
        user_list = uh.config['testers']
        keys_to_check = uh.config['keys_to_remove']
        for user in user_list:
            u = uc.create_by_args(user)
            ud = uf.user_to_dict(u)
            for ktc in keys_to_check:
                self.assertEqual(ud[ktc], getattr(u, ktc))
            self.assertEqual(ud['user_key'], u.key.urlsafe())

