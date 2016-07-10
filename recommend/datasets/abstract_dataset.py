# -*- coding: utf-8 -*-
'''
Created on Jul 5, 2016

@author: yukoga
'''

from abc import abstractmethod
from recommend.base.base_abstract import BaseAbstract


class AbstractDataset(BaseAbstract):
    '''
    Abstract class for kinds of dataset class.
    '''

    @abstractmethod
    def fetch_data(self, query=None):
        pass

    @abstractmethod
    def fetch_table_data(self, table_name=None, file_name=None):
        pass
