""" TFA Service as a plugin """
import logging

class Validator(object):
    """ Validator class """
    def __init__(self, user=None, params=None):
        self.user = user
        self.params = params

    def validate(self):
        """ Method to execute tfa validation """
        logging.info(self.user)
        logging.info(self.params)
        return True
