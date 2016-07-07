# -*- coding: utf-8 -*-
'''
Created on Jul 5, 2016

@author: yukoga
'''

from abc import ABCMeta


class BaseAbstract(object):
    '''
    Base Abstract Class.
    '''
    __metaclass__ = ABCMeta

    @classmethod
    def __subclasshook__(self, cls, C):
        if cls is self.__class__.__name__:
            if all(cls.__abstractmethods__ in B.__dict__ for B in C.__mro__):
                return True
        raise NotImplementedError
