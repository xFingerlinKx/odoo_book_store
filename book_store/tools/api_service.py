# 1 : imports of python lib
import requests
import logging
import traceback

# 2 :  imports of odoo
from odoo.tools import config
from odoo.exceptions import ValidationError

# 3 :  imports of odoo modules

# 4 :  imports from custom modules
from . import constants


_logger = logging.getLogger(__name__)


class ApiService(object):
    """
    Base class for make custom Book API request and get response.
    """

    def __init__(self, env):
        self.env = env
        self.request_verify = False
        self.request_timeout = 10
        self.absolute_url = self._get_absolute_url()
        super(ApiService, self).__init__()

    def get_book_api_response(self, isbn):
        """
        Get request URL and make request to get response data.

        :param isbn: {str} book ISBN
        :return: {dict, str} response data content and error log if something wrong has happened
        """
        url = self._get_request_url(isbn=isbn)
        response_content_dict, response_error_log = self._send_request(url=url)
        return response_content_dict, response_error_log

    def _get_request_url(self, isbn, jscmd='data', request_format='json'):
        """
        Get full request URL.
        Book API documentation - https://openlibrary.org/dev/docs/api/books.

        :param isbn: {str} book ISBN
        :param jscmd: {str} detail level of service response
        :param request_format: {str} response format
        :return: {str} full URL for request
        """
        absolute_url = self._get_absolute_url()
        return absolute_url + f'/api/books?bibkeys=ISBN:{isbn}&jscmd={jscmd}&format={request_format}'

    # noinspection PyMethodMayBeStatic
    def _get_absolute_url(self):
        """
        Get absolute URL of API service from config file.

        :return: {str} absolute URL of API service
        """
        absolute_url = config.get('books_api_service_url', '')
        if not absolute_url:
            raise ValidationError('The URL for sending the request is not set!')
        return absolute_url

    def _send_request(self, url, params=None, headers=None, verify=True, timeout=10):
        """
        Send request.

        :param url: {str} request URL
        :param params: {dict} the query parameters
        :param headers: {dict} the HTTP headers
        :param verify: {bool} (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use
        :param timeout: {int} (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:'(connect timeout,
            read timeout) <timeouts>' tuple
        :return: {dict, str} response data content and error log if something wrong has happened
        """
        response_content = {}
        response_error_log = ''
        try:
            response = self.__send_request(url, params, headers, verify, timeout)
            if response.status_code in constants.RESPONSE_STATUS_CODES_LIST:
                response_content = response.json()
            else:
                response_content = {}
        except Exception as e:
            error = e
            full_error = traceback.format_exc()
            response_error_log = str(error.__str__) + '\n\n' + full_error
        return response_content, response_error_log

    @staticmethod
    def __send_request(url, params, headers, verify, timeout):
        """
        Send request and return response.

        :param url: {str} request URL
        :param params: {dict} the query parameters
        :param headers: {dict} the HTTP headers
        :param verify: {bool} (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use
        :param timeout: {int} (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:'(connect timeout,
            read timeout) <timeouts>' tuple
        :return: response object
        """
        return requests.get(url=url, params=params, headers=headers, verify=verify, timeout=timeout)
