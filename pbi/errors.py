""" Personal custom error handling """
import logging
import traceback

import ndb_json

ERROR_DICT = {}

class CustomException(Exception):
    """ Our own base custom exception """
    def __init__(self, error_code=None, details=None, response=None, *args, **kwargs):
        self.__error_code = error_code
        self.__details = details
        self.__response = response
        super(CustomException, self).__init__(*args, **kwargs)

    def __str__(self):
        return repr(self.__details)

    @property
    def error_code(self):
        """ Error_code property"""
        return self.__error_code

    @property
    def details(self):
        """ Details property"""
        return self.__details

    @property
    def response(self):
        """ Response property"""
        return self.__response

    def respond(self, response=None, status=500):
        """ Mechanism for turning custom exception into
        restful response """
        if response is None:
            response = self.response
        err = ErrorReturn(
            response,
            error_code=self.error_code,
            details=self.details)
        logging.info("CE.r")
        logging.info(self.details)
        err.handle_response(status)


class ErrorReturn(object):
    """ Class that handles html response """
    def __init__(self, response, error_code=None, details=None):
        self.response = response
        self.__error_code = error_code
        self.__details = details

    @property
    def error_package(self):
        """ Error package property
        handles formatting based on what was set """
        return_package = {}
        if self.__error_code:
            return_package['code'] = self.__error_code
            return_package['description'] = ERROR_DICT[self.__error_code]
        else:
            return_package['code'] = 'N/A'
            return_package['description'] = 'N/A'

        if self.__details:
            return_package['details'] = self.__details
        return return_package

    def handle_response(self, status=None):
        """ General repsonse handler """
        logging.info("ER.h_r")
        logging.info(self.__details)
        if int(status) == 200:
            self._handle_200()
        elif int(status) == 400:
            self._handle_400()
        elif int(status) == 401:
            self._handle_401()
        elif int(status) == 403:
            self._handle_403()
        elif int(status) == 404:
            self._handle_404()
        elif int(status) == 500:
            self._handle_500()

    # Default to walk ourselves out of some of this error handling
    def _handle_200(self):
        error_info = self.error_package
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['content-type'] = "application/json"
        self.response.write(ndb_json.dumps(error_info))
        self.response.set_status(200)

    def _handle_400(self):
        logging.info("400 in our own method")
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        error_info = self.error_package
        self.response.headers['content-type'] = "application/json"
        self.response.write(ndb_json.dumps(error_info))
        self.response.set_status(400)
        traceback.print_stack()

    def _handle_401(self):
        logging.info("401 in our own method")
        error_info = self.error_package
        self.response.headers['content-type'] = "application/json"
        self.response.write(ndb_json.dumps(error_info))
        self.response.set_status(401)
        traceback.print_stack()

    def _handle_403(self):
        logging.info("403 in our own method")
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        error_info = self.error_package
        self.response.headers['content-type'] = "application/json"
        self.response.write(ndb_json.dumps(error_info))
        self.response.set_status(403)
        traceback.print_stack()

    def _handle_404(self):
        logging.info("404 in our own method")
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        error_info = self.error_package
        self.response.headers['content-type'] = "application/json"
        self.response.write(ndb_json.dumps(error_info))
        self.response.set_status(404)
        traceback.print_stack()

    def _handle_500(self):
        logging.info("500 in our own method")
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        error_info = self.error_package
        self.response.headers['content-type'] = "application/json"
        self.response.write(ndb_json.dumps(error_info))
        self.response.set_status(500)
        traceback.print_stack()
