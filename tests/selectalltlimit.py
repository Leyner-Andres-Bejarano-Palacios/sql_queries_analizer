#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import logging
from queryTestAB import QueryTestAB


"""
#-------------------------------------------------------------------------
#----------------- Implementation class, with in query ------------------
#---------------- @author: Sebastian Lopez (slvalen) ---------------------
# components:
#           - Properties
#           - Methods
# usage:
#       vTest = selectalltlimit(properties)
#       vResult = vTest.fn_execute
#-------------------------------------------------------------------------
"""
class Selectalltlimit(QueryTestAB):
    LIMIT_EXCEEDED = "Se ha excedido el limite en la validacion {}"
    TEST_SUCCEEDED = "Se termina de forma exitosa la prueba de {}"
    TEST_DESCRIPTION = "Test de {} en las consultas"
    START = "El test inicia la ejecucion de {}"
    def __init__(self, query, logger, properties):
        super(Selectalltlimit, self).__init__(query,logger, properties)
        self._vName = self.__class__.__name__
        self._vQuery = self.fn_preprocess_query(query)
        self._vLogger.info(self.TEST_DESCRIPTION.format(self._vName))
        self.__vSelectalltlimit = int(properties['selectalltlimit'])
        self.__vSelectallRegex = properties['selectallregex']
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
        self._vLogger.info(self.START.format(self._vName))
        vSelectallQuantity = 0
        pattern = self.__vSelectallRegex
        matches = re.finditer(pattern, self._vQuery, flags=re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            if isinstance(match.group(), str):
                if  ((match.group()+"from").count("* from") > 0) or \
                    (match.group().count("*,")     > 0) or \
                    (match.group().count("* ,")    > 0) or \
                    (match.group().count(",*")     > 0) or \
                    (match.group().count(", *")    > 0) :
                    vSelectallQuantity +=   len(match.group())
        if vSelectallQuantity > self.__vSelectalltlimit:
            self._vLogger.info(self.LIMIT_EXCEEDED.format(self._vName))
            self._vResult = False
            return False,vSelectallQuantity,"select * found"
        self._vLogger.info(self.TEST_SUCCEEDED.format(self._vName))
        self._vResult = True
        return True,vSelectallQuantity,"select * found"