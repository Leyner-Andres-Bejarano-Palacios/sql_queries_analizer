#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import ast as tree
from routineValidatorDA import RoutineValidatorDA
from routineValidatorUT import RoutineValidatorUT as Utilities


"""
#-------------------------------------------------------------------------
#-------------------------- Business logic, only operations --------------
#---------------- @author: Leyner Bejarano (labejara) --------------------
# components:
#           - Constants
#           - instance methods
# usage:
#       obj = routineValidatorBL(loggerInstance,propertiesPath)
#       obj.fn_get_queries(...)
#-------------------------------------------------------------------------
"""

class RoutineValidatorBL:
    DETECTED_QUERIES = "Se detectan {} consultas con malas practicas"

    def __init__(self, logger, vArgs):
        self.__vLogger = logger
        self.__vDataLayer = RoutineValidatorDA(logger, vArgs)
        self.__vName = self.__class__.__name__
        self.__vProperties = self.__vDataLayer.fn_prepare_properties(vArgs.vPropertiesPath)
        self.__vRoutineName = vArgs.vRoutineName

    @property
    def vDataLayer(self):
        return self.__vDataLayer


    """
    #-------------------------------------------------------------------------
    #--- Instance method to get not compliant queries from a list of queries -
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    # inputs:
    #       - self: implicit, instance
    #       - queries: Impala queries list
    # output:
    #       vBadQueries: list, non compliant queries
    # usage:
    #       obj.fn_get_bad_queries(queries)
    #-------------------------------------------------------------------------
    """

    def fn_get_queries(self):
        return self.__vDataLayer.fn_get_queries()


    def fn_get_bad_queries(self, queries):
        vBadQueries = []
        vBadQueriesPartial = []
        for query in queries:
            vBadQueriesPartial.extend(self.fn_check_rule_violation(query))
        vBadQueries = list(filter(lambda query: query["ruleViolation"] ==  False,vBadQueriesPartial))
        return vBadQueries

    def __fn_type_bad_query(self,ar_class):
        vDictionary=tree.literal_eval(self.__vProperties['mappingtypebadquerys'])
        return vDictionary.get(ar_class," ")


    def  fn_check_rule_violation(self,ar_query):
        vBadQueriesPartial = []
        vTests = self.__vDataLayer.fn_read_classes()
        for vTest in vTests:
            try:
                vUnit = vTest(ar_query[1],self.__vLogger, self.__vProperties)
                vResult,vCounter,vDetected = vUnit.fn_execute()
                vBadQueriesPartial.append({"consulta":ar_query[1], 
                                            "rule":self.__fn_type_bad_query(vUnit.__class__.__name__),
                                            "detected":vDetected, 
                                            "fileName":ar_query[0],
                                            "ruleViolation":vResult})
            except Exception as ex:
                vTrace = str(ex) + str(sys.exc_info()[1])
                Utilities.fn_write_log(self.__vLogger, vTrace, logging.INFO, self.__vName)
                raise
        return vBadQueriesPartial

    def  fn_write_bad_query(self,vBadQueries):
        vRules=[]
        vFileName=[]
        vQueries=[]
        if len(vBadQueries) < 1:
            with open("hallazgos/"+self.__vRoutineName+".txt", "w+") as f:
                f.write('#################################################\n')
                f.write('        ########          SIN HALLAZGOS       ###########\n')
                f.write('#################################################\n')
                f.write('\n')
        else:
            with open("hallazgos/"+self.__vRoutineName+".txt", "w+") as f:
                
                for queryIndex in range(len(vBadQueries)):
                    vRules.append(vBadQueries[queryIndex]['rule']+' \n')
                    vFileName.append(vBadQueries[queryIndex]['fileName']+' \n')
                    vQueries.append(vBadQueries[queryIndex]['fileName']+' \n' + vBadQueries[queryIndex]['consulta']+' \n\n')
                strRules="".join(list(set(vRules)))
                strFileName="".join(list(set(vFileName)))
                strQueries="####################FILE#################################\n".join(list(set(vQueries)))
                f.write('*******************************************************\n')
                f.write('INFORME MALAS PRACTICAS\nCELULA LZ\n')
                f.write('*******************************************************\n')
                f.write('SE DETECTAN '+str(len(vBadQueries))+'  HALLAZGO(S) \n')
                f.write('\n****RUTINA******\n'+self.__vRoutineName+"\n")
                f.write('\n****HALLAZGO****\n'+strRules)
                f.write('\n****FILES*******\n'+strFileName)
                f.write('\n****Queries*****\n'+strQueries)        
        return None



