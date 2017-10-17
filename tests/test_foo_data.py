import logging
from pprint import PrettyPrinter

from datetime import datetime
from dateutil.parser import parse
from freezegun import freeze_time
from libfaketime import fake_time, reexec_if_needed

from google.appengine.ext import ndb

from pbi.data.foo import FooAccess
from pbi.data.user import UserCreator, UserValidator, UserFormatter
from pbi.errors import CustomException

from helpers import Helpers, UserHelpers

# libfaketime needs to be preloaded by the dynamic linker.
# This will exec the same command, but with the proper environment variables set.
# You can also skip this and manually manage your env (see "How to avoid re-exec").
reexec_if_needed()

class TestFooAccess(Helpers):

    @fake_time('2014-01-01T00:00:00')
    def test_foo_create(self):
        self._start_()
        uh = UserHelpers()
        uh.create_users()
        user_list = uh.user_list
        fa = FooAccess()
        for user in user_list:
            f = fa.create(user=user.key, firstname=user.firstname)
            self.assertEqual(datetime.now(), f.createdDate)

    def test_foo_update_with_fake_time(self):
        self._start_()
        uh = UserHelpers()
        uh.create_users()
        user_list = uh.user_list
        fa = FooAccess()
        pp = PrettyPrinter()
        for user in user_list:
            f = fa.create(user=user.key, firstname=user.firstname)
            with fake_time('2014-01-01 00:00:00'):
                fa.update(f)
                self.assertEqual(datetime.now(), f.updatedDate)
        self.assertTrue(False)

    def test_foo_update_with_freeze(self):
        self._start_()
        uh = UserHelpers()
        uh.create_users()
        user_list = uh.user_list
        fa = FooAccess()
        pp = PrettyPrinter()
        for user in user_list:
            f = fa.create(user=user.key, firstname=user.firstname)
            with freeze_time('2014-01-01 00:00:00'):
                fa.update(f)
                self.assertEqual(datetime.now(), f.updatedDate)
                pp.pprint(f)
        self.assertTrue(False)

    @freeze_time('2014-01-01T00:00:00')
    def test_foo_create_freeze_time(self):
        self._start_()
        uh = UserHelpers()
        uh.create_users()
        user_list = uh.user_list
        fa = FooAccess()
        pp = PrettyPrinter()
        for user in user_list:
            f = fa.create(user=user.key, firstname=user.firstname)
            self.assertEqual(datetime.now(), f.createdDate)
        self.assertTrue(False)
