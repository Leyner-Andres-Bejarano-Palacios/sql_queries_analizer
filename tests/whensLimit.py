#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import logging
from queryTestAB import QueryTestAB
from bigdatacompanypy.codeanalizer import analizerutil
"""
#-------------------------------------------------------------------------
#----------------- Implementation class, whens for case in query ------------------
#---------------- @author: Sebastian Lopez (slvalen) ---------------------
# components:
#           - Properties
#           - Methods
# usage:
#       vTest = WhensLimit(properties)
#       vResult = vTest.fn_execute
#-------------------------------------------------------------------------
"""


class WhensLimit(QueryTestAB):
    LIMIT_EXCEEDED = "Se ha excedido el limite en la validacion {}"
    TEST_SUCCEEDED = "Se termina de forma exitosa la prueba de {}"
    TEST_DESCRIPTION = "Test de {} en las consultas"
    START = "El test inicia la ejecucion de {}"
    
    def __init__(self, query, logger, properties):
        super(WhensLimit, self).__init__(query,logger, properties)
        self._vName = self.__class__.__name__
        self._vQuery = self.fn_preprocess_query(query,)
        self._vLogger.info(self.TEST_DESCRIPTION.format(self._vName))
        self.__vWhensLimit = int(properties['whenslimit'])


    @property
    def vName(self):
        return self._vName
    @property
    @classmethod
    def DESCRIPTION(cls):
        return cls.TEST_DESCRIPTION.format(cls._vName)
    @property
    def vQuery(self):
        return self._vQuery
    @property
    def vResult(self):
        return self._vResult
    @property
    def vProperties(self):
        return self._vProperties

    def fn_detect_bad_subquery(self,query):
        vWhenLimitExceed = 0
        pattern = self._vProperties['whenregex']
        matches = re.finditer(pattern, query, flags=re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            if (isinstance(match.group(), str)) and (match.group().count(" when ") > self.__vWhensLimit):
                vWhenLimitExceed = 1
                break
        return vWhenLimitExceed

    def fn_preprocess_query(self,query):
        vStringsToRemove = []
        patternUnicode = self._vProperties['unilinecomment']
        patternMultiLine = self._vProperties['multilinecomment']
        patternSingleQuotedText = self._vProperties['singlequotedtext'].replace('"','').strip()
        patternDoubleQuotedText = self._vProperties['doublequotedtext'].replace("'","").strip()
        matches = re.finditer(patternUnicode, query, flags=re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            vStringsToRemove.append(match.group())
        matches = re.finditer(patternMultiLine, query, flags=re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            vStringsToRemove.append(match.group())
        matches = re.finditer(patternSingleQuotedText, query, flags=re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            vStringsToRemove.append(match.group())
        matches = re.finditer(patternDoubleQuotedText, query, flags=re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            vStringsToRemove.append(match.group())
        for subString in vStringsToRemove:
            query = query.replace(subString,"")
        query = query.lower()
        query = re.sub(r'\r+',' ', query)
        query = re.sub(r'\n+',' ', query)
        query = re.sub(r'\t+',' ', query)
        query = re.sub(r' +', ' ', query)
        return query


    def fn_execute(self):
        vWhenLimitExceed = 0
        self._vLogger.info(self.START.format(self._vName))
        vWhenLimitExceed = self.fn_detect_bad_subquery(self._vQuery)
        if vWhenLimitExceed > 0:
            self._vLogger.info(self.LIMIT_EXCEEDED.format(self._vName))
            self._vResult = False
            return False,vWhenLimitExceed,"more than "+str(self.__vWhensLimit)+" when words found"
        self._vLogger.info(self.TEST_SUCCEEDED.format(self._vName))
        self._vResult = True
        return True,vWhenLimitExceed,"more than "+str(self.__vWhensLimit)+" when words found"
 
