import logging
from pprint import PrettyPrinter

from datetime import datetime
from dateutil.parser import parse
from utils import freeze_time

from google.appengine.ext import ndb

from pbi.data.foo import FooAccess
from pbi.data.user import UserCreator, UserValidator, UserFormatter
from pbi.errors import CustomException

from helpers import Helpers, UserHelpers


class TestFooAccess(Helpers):

    @freeze_time('2014-01-01T00:00:00')
    def test_foo_update_with_freeze(self):
        self._start_()
        uh = UserHelpers()
        uh.create_users()
        user_list = uh.user_list
        fa = FooAccess()
        pp = PrettyPrinter()
        for user in user_list:
            f = fa.create(user=user.key, firstname=user.firstname)
            fa.update(f)
            self.assertEqual(datetime.now(), f.updatedDate)
            """
            with freeze_time('2014-01-01 00:00:00'):
                fa.update(f)
                self.assertEqual(datetime.now(), f.updatedDate)
                pp.pprint(f)
            """
        #self.assertTrue(False)

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
            logging.info("foo created: " + str(f.createdDate))
            logging.info("now: " + str(datetime.now()))
            self.assertEqual(datetime.now(), f.createdDate)
            """
            with freeze_time('2014-01-01 00:00:00'):
                f = fa.create(user=user.key, firstname=user.firstname)
                self.assertEqual(datetime.now(), f.createdDate)
            """
        #self.assertTrue(False)
