#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
#-------------------------------------------------------------------------
# Author: Leyner Andres Bejarano PAlacios 
# Description: Routine queries with bad practices detection.
#
# Run: ./routineValidator.py -p <properties filepath>
#
# v0.1
# Modification:
# Description:
#-------------------------------------------------------------------------
"""

import sys
import copy
import logging
from routineValidatorUT import ArgParser
from routineValidatorBL import RoutineValidatorBL
from routineValidatorUT import RoutineValidatorUT as Utilities


"""
#-------------------------------------------------------------------------
#------ Main class, It has constants and main operational methods --------
#---------------- @author: Leyner Bejarano (labejara) --------------------
# components:
#           - Constants
#           - instance methods
# methods:
#           - fn_execute(): Running point
# usage:
#       obj = ImpalaQueries(propertiesPath)
#       obj.fn_execute('/path/to/propeties/file.properties')
#-------------------------------------------------------------------------
"""


class RoutineValidator:
    NO_BAD_QUERIES = 'No se detecta consultas con malas practicas'
    NO_ERROR_CODE = 0
    ANALYZED_QUERIES="Cantidad de consultas a revisar: "
    def __init__(self, vArgs):
        self.__vLogger = Utilities.fn_prepare_logging()
        self.__vBusinessLayer = RoutineValidatorBL(self.__vLogger, vArgs)
        self.__vName = self.__class__.__name__

    """
    #-------------------------------------------------------------------------
    #-------------------- Instance method to run script ----------------------
    #---------------- @author: Leyner Bejarano (labejara) --------------------
    # inputs:
    #       - self: implicit, instance
    # output:
    #       exit
    # usage:
    #       obj.fn_execute('/path/to/propeties/file.properties')
    #-------------------------------------------------------------------------
    """
    def fn_execute(self):
        vQueries = self.__vBusinessLayer.fn_get_queries()
        Utilities.fn_write_log(self.__vLogger, self.ANALYZED_QUERIES + str(len(vQueries)) \
                , logging.INFO, self.__vName)
        vBadQueries = self.__vBusinessLayer.fn_get_bad_queries(vQueries)
        vBadQueries = self.__vBusinessLayer.fn_write_bad_query(vBadQueries)


if __name__ == '__main__':
    vArgs = ArgParser.fn_get_args()
    vExecutor = RoutineValidator(vArgs)
    __vLogger = Utilities.fn_prepare_logging()
    try:
        vExecutor.fn_execute()
    except Exception as ex:
        vTrace = str(ex) + str(sys.exc_info()[1])
        Utilities.fn_write_log(__vLogger, vTrace, logging.ERROR, "[routineValidator-MainProcess]")
        raise



