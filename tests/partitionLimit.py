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
#       vTest = WithLimit(properties)
#       vResult = vTest.fn_execute
#-------------------------------------------------------------------------
"""




class PartitionLimit(QueryTestAB):
    LIMIT_EXCEEDED = "El query contiene zonas raw y no usa particion"
    TEST_SUCCEEDED = "Se termina de forma exitosa la prueba de {}"
    TEST_DESCRIPTION = "Test de {} en las consultas"
    START = "El test inicia la ejecucion de validacion de particiones"
    def __init__(self, query, logger, properties):
        super(PartitionLimit, self).__init__(query,logger, properties)
        self._vName = self.__class__.__name__
        self._vLogger.info(self.TEST_DESCRIPTION.format(self._vName))
        self._vQuery = self.fn_preprocess_query(query)
        self.__vPartitionLimit = int(properties['partitionlimit'])
        self.__vDataBasesRaw=properties['databasesraw'].split(",")
        self.__vPatternExtractSegment=properties['patternextractsegment'].split(",")
        self.__vPatternValidateSegment=properties['patternvalidatesegment'].split(",")

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


    def __fn_find_referenced_tables(self,ar_sql,__vPatternExtractSegment,__vDataBasesRaw):
        vListReferencedTablesTemp=[]
        vListReferencedTables = []
        for indexpattern in __vPatternExtractSegment:
            for database in __vDataBasesRaw:
                pattern = indexpattern.strip()+'[\s]('+database+'\.[a-z0-9\_\-]*)'
                matches = re.finditer(pattern, ar_sql)
                for matchNum , match in enumerate(matches, start=1):
                    vListReferencedTablesTemp.append(match.group())
        for text in vListReferencedTablesTemp:
            vListReferencedTables.extend([value for value in text.split() if "." in value ])
        return vListReferencedTables



    def __fn_find_referenced_partition(self,ar_sql,__vPatternExtractSegment):
        vListReferencedPartition=[]
        for indexpattern in __vPatternExtractSegment:
            if 'where' not in indexpattern:
                pattern = '(?<='+indexpattern.strip()+')([\s\S]*?)(?=[^\s]*year[\s]*=)'
                matches = re.finditer(pattern, ar_sql, flags=re.MULTILINE)
                for matchNum, match in enumerate(matches, start=1):
                    vListReferencedPartition.append(match.group())
        return vListReferencedPartition


    def __fn_find_table_aliases(self,ar_sql,vListReferencedTables):
        vReferencedTablesAliases = {}
        vSetReferencedTables =  set(vListReferencedTables)
        for table in vSetReferencedTables:
            pattern = '[\s]'+table.replace(".","\.").strip()+'[^\s]*[\s][a][s][\s]([^\(\)\s]*)|[\s]'+table.replace(".","\.").strip()+'[^\s]*[\s]([^\(\)\s]*)'
            print(pattern)
            matches = re.finditer(pattern, ar_sql, flags=re.MULTILINE)
            vListTableAliases = []
            for matchNum, match in enumerate(matches, start=1):
                vListTableAliases.append(match.group())
            if vListTableAliases:
                vReferencedTablesAliases[table] = vListTableAliases
        return vReferencedTablesAliases




    def __fn_get_table_refering_partition(self,ar_sql,vListReferencedPartition,__vPatternExtractSegment):
        vListTablesReferingPartitionTemp = []
        vListTablesReferingPartition = []
        for reference_partition in vListReferencedPartition:
            for indexpattern in __vPatternExtractSegment:
                pattern = '[\s]'+indexpattern.strip()+'[\s\S]*?(?=[^\s]*year[\s]*=)'
                matches = re.findall(pattern, ar_sql, flags=re.MULTILINE)
                if len(matches) > 0:
                    vListTablesReferingPartitionTemp.extend([value for value in matches if "." in value])
        for text in vListTablesReferingPartitionTemp:
            vListTablesReferingPartition.extend([value for value in text.split() if "." in value ]) 
        return vListTablesReferingPartition

    def __fn_replace_alias_for_table(self,vListTablesReferingPartition,vReferencedTablesAliases):
        for listIndex in range(len(vListTablesReferingPartition)):
            for key in vReferencedTablesAliases:
                if vListTablesReferingPartition[listIndex] in vReferencedTablesAliases[key]:
                    vListTablesReferingPartition[listIndex] = key
        return vListTablesReferingPartition

    def __fn_remove_no_raw_table(self,vListTablesReferingPartition,__vDataBasesRaw):
        vListRawTablesReferingPartition = []
        for listIndex in range(len(vListTablesReferingPartition)):
            for database in __vDataBasesRaw:
                if database == vListTablesReferingPartition[listIndex].split(".")[0]:
                    vListRawTablesReferingPartition.append( vListTablesReferingPartition[listIndex] )
        return vListRawTablesReferingPartition
            

    def __fn_check_table_partition_balance(self,vListRawTablesReferingPartition,vListReferencedTables):
        vSegmentsPartition = 0
        vCountReferencedTables = {}
        vCountTablesReferencingPartition = {}
        for tableName in set(vListRawTablesReferingPartition):
            vCountTablesReferencingPartition[tableName] = vListRawTablesReferingPartition.count(tableName)
        for tableName in set(vListReferencedTables):
            vCountReferencedTables[tableName] = vListReferencedTables.count(tableName)

        for key in vCountReferencedTables:
            if key not in vCountTablesReferencingPartition:
                vSegmentsPartition = 1
                break
            elif vCountReferencedTables[key] > vCountTablesReferencingPartition[key]:
                vSegmentsPartition = 1
                break
                
        return vSegmentsPartition

    
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
        self._vLogger.info(self.START)
        vSegmentsPartition = 0
        vListReferencedTables = self.__fn_find_referenced_tables(self._vQuery,self.__vPatternExtractSegment,self.__vDataBasesRaw)
        vListReferencedPartition = self.__fn_find_referenced_partition(self._vQuery,self.__vPatternExtractSegment)
        vReferencedTablesAliases = self.__fn_find_table_aliases(self._vQuery,vListReferencedTables)
        vListTablesReferingPartition = self.__fn_get_table_refering_partition(self._vQuery,vListReferencedPartition,self.__vPatternExtractSegment)
        vListTablesReferingPartition = self.__fn_replace_alias_for_table(vListTablesReferingPartition,vReferencedTablesAliases)
        vListRawTablesReferingPartition = self.__fn_remove_no_raw_table(vListTablesReferingPartition,self.__vDataBasesRaw)
        if not vListReferencedTables:
            vSegmentsPartition = 0
        elif not vListReferencedPartition:
            vSegmentsPartition = 1
        else:
            vSegmentsPartition = self.__fn_check_table_partition_balance(vListRawTablesReferingPartition,vListReferencedTables)
        if vSegmentsPartition > self.__vPartitionLimit:
            self._vLogger.info(self.LIMIT_EXCEEDED)
            self._vResult = False
            return False,vSegmentsPartition,"Work in progress"
        self._vLogger.info(self.TEST_SUCCEEDED.format(self._vName))
        self._vResult = True
        return True,vSegmentsPartition,"Work in progress"
