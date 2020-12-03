#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import tests
import inspect
import logging
import importlib
from bigdatacompanypy import Properties
from routineValidatorUT import RoutineValidatorUT as Utilities


"""
#-------------------------------------------------------------------------
#----------- Data access, only retrive info from sources and APIs --------
#---------------- @author: Leyner Bejarano (labejara) --------------------
# components:
#           - Constants
#           - instance methods
# usage:
#       obj = routineValidatorDA(loggerInstance,propertiesPath)
#       obj.fn_get_queries(...)
#-------------------------------------------------------------------------
"""


class RoutineValidatorDA:
    GETTING_ROUTINE_QUERIES = "Recuperando consultas de archivos .sql en la rutina"
    PROPERTIES_ERROR = "Error durante la carga de propiedades, revisar archivo"
    INCOMPLETE_PROPERTIES = "Propiedades incompletas en el archivo de configuracion"
    PROPERTIES_INIT = "Iniciando revisión de propiedades"
    LOADING_FILE_ERROR = "Error al cargar el archivo de propiedades, validar ruta"

    def __init__(self, logger, vArgs):
        self.__vlogger = logger
        self.__vName = self.__class__.__name__
        self.__vProperties = self.fn_prepare_properties(vArgs.vPropertiesPath)
        self.__vRoutinePath = vArgs.vRoutinePath


    def fn_get_properties(self):
        return self.__vProperties

    """     
    #-------------------------------------------------------------------------
    # Instance method to get queries from Cloudera manager API, parse to dict 
    #---------------- @author: Leyner Bejarano (labejara) ---------------------
    # inputs:
    #       - self: implicit, instance
    # output:
    #       vSqlRoutes : list of routes or exception
    # usage:
    #       obj.fn_get_routes()
    #-------------------------------------------------------------------------
    """
    def fn_get_routes(self):
        Utilities.fn_write_log(self.__vlogger,self.GETTING_ROUTINE_QUERIES, logging.INFO, self.__vName)
        vSqlRoutes = []
        vSqlRoutesTemp = []
        vError=""
        try:
            for root, _, files in os.walk(self.__vRoutinePath):
                vSqlRoutesTemp = [os.path.join(root,file) for file in files if file.endswith(".sql") or file.endswith(".SQL")]
                vSqlRoutes.extend(vSqlRoutesTemp)
            return vSqlRoutes
        except Exception as ex:
            vError = str(ex) + str(sys.exc_info()[1])
            Utilities.fn_write_log(self.__vlogger,"error detectado : "+vError, logging.ERROR, self.__vName)
            raise
            sys.exit(1)


    """     
    #-------------------------------------------------------------------------
    # Instance method to get queries from Cloudera manager API, parse to dict 
    #---------------- @author: Leyner Bejarano (labejara) ---------------------
    # inputs:
    #       - self: implicit, instance
    # output:
    #       vPdfsRoute : list of tuples (routes,query) or exception
    # usage:
    #       obj.fn_get_text()
    #-------------------------------------------------------------------------
    """
    def fn_get_queries(self):
        vSqlRoutes = self.fn_get_routes()
        vQueries = []
        vError=""
        try:
            for route in vSqlRoutes:
                for query in open(route).read().split(';'):
                    vQueries.append((route,query))
            return vQueries
        except Exception as ex:
            vError = str(ex) + str(sys.exc_info()[1])
            Utilities.fn_write_log(self.__vlogger,"error detectado : "+vError, logging.ERROR, self.__vName)
            raise
            sys.exit(1)

    """
    #-------------------------------------------------------------------------
    #--------- Private instance method to read properties from file ----------
    #---------------- @author: Leyner Bejarano (labejara) --------------------
    # inputs:
    #       - self: implicit, instance
    #       - propertiesPath: Properties file path - string
    # output:
    #       Json, properties dict
    # usage:
    #       Only for internal use
    #-------------------------------------------------------------------------
    """
    def fn_prepare_properties(self, propertiesPath):
        vProperties = {}
        try:
            Utilities.fn_write_log(self.__vlogger,self.PROPERTIES_INIT, logging.INFO, self.__vName)
            vProperties = Properties(propertiesPath)
        except Exception as ex:
            Utilities.fn_write_log(self.__vlogger, str(ex), logging.ERROR, self.__vName)
            raise Exception(self.LOADING_FILE_ERROR)
        vGlobalProps = vProperties["GLOBAL"]
        return vGlobalProps
    """
    #-------------------------------------------------------------------------
    #--------- Instance method to read available tests in test module --------
    #---------------- @author: Leyner Bejarano (labejara) --------------------
    # inputs:
    #       - self: implicit, instance
    # output:
    #       - vClasses: List, Class objects list
    # usage:
    #       obj.fn_read_classes()
    #-------------------------------------------------------------------------
    """
    def fn_read_classes(self):
        vModule = importlib.import_module('tests')
        vClasses = []
        for vName, vComponent in inspect.getmembers(vModule):
            if inspect.isclass(vComponent):
                Utilities.fn_write_log(self.__vlogger,"Test cargado: {} ".format(vName), \
                    logging.INFO, self.__vName)
                vClasses.append(vComponent)
        return vClasses