#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
from abc import ABCMeta, abstractmethod, abstractproperty

"""
#-------------------------------------------------------------------------
#-------------------- Abstract class, test requirements ------------------
#---------------- @author: Sebastian Lopez (slvalen) ---------------------
# components:
#           - Abstract methods
#           - Abstract properties
# usage:
#       Implement a descendent
#-------------------------------------------------------------------------
"""




class QueryTestAB:
    __metaclass__ = ABCMeta
    def __init__(self, query, logger, properties):
        self._vQuery = query.lower()
        self._vQuery = repr(self._vQuery).replace(r'\r',' ')
        self._vQuery = repr(self._vQuery).replace(r'\\n',' ')
        self._vQuery = repr(self._vQuery).replace(r'\\\\t',' ')
        self._vQuery = re.sub(r' +', ' ', self._vQuery)
        self._vResult = None
        self._vLogger = logger
        self._vProperties = properties
    @abstractproperty
    def vName(self):
        pass
    @abstractproperty
    def vQuery(self):
        pass
    @abstractproperty
    def vResult(self):
        pass
    @abstractproperty
    def vProperties(self):
        pass
    @abstractmethod
    def fn_execute(self):
        pass
    @abstractproperty
    @classmethod
    def DESCRIPTION(cls):
        pass



