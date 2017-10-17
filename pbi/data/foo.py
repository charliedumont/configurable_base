import logging
from pprint import PrettyPrinter

from datetime import datetime

from google.appengine.ext import ndb

from models import Foo
from pbi.errors import CustomException

class FooAccess(object):

    def create(self, user=None, firstname=None):
        try:
            f = Foo()
            f.user = user
            f.firstname = firstname
            f.put()
        except Exception as e:
            details = str(e)
            logging.info(details)
            raise CustomException(details=details)
        return f

    def update(self, foo):
        try:
            foo.registeredDate = datetime.now()
            foo.updatedDate = datetime.now()
        except Exception as e:
            details = str(e)
            logging.info(details)
            raise CustomException(details=details)
        return foo

