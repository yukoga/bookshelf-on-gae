# -*- coding: utf-8 -*-
'''
Created on Jul 26, 2016

@author: yukoga
'''

import gav4
import pandas as pd
import re

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from .abstract_dataset import AbstractDataset
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from setuptools.package_index import Credential


class GoogleAnalytics(AbstractDataset):
    '''
    Retrieve data from Google Analytics Core Reporting API.
    Then build and return its pandas.DataFrame.
    '''

    def __init__(self, params=None):
        '''
        Constructor
        '''
        # TODO: exception handling for required parameters.
        self.api_name = params['api_name']
        self.api_version = params["api_version"]
        self.scope = params["scope"]
        self.key_file = params["key_file_location"]
        self.service_account_email = params["service_account_email"]

        credentials = ServiceAccountCredentials.from_p12_keyfile(
            self.service_account_email, self.key_file, scopes=self.scope)
        http = credentials.authorize(httplib2.Http())
        self.service = build(self.api_name, self.api_version, http=http)
        self.total = None
        self.features = None
        self.target = None

    def fetch_data(self, query=None):
        pass

    def fetch_table_data(self, table_name=None, file_name=None):
        pass
