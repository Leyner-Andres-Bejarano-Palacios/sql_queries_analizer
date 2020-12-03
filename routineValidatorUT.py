#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import argparse
import logging, time
from bigdatacompanypy import FlowModule

"""
#--------------------------------------------------------------------------
#------------------ Utilities, only classmethods for help -----------------
#---------------- @author: Leyner Bejarano (labejara) ---------------------
# components:
#           - Constants
#           - class methods
# usage:
#       vLogger = routineValidatorUT.fn_prepare_logging()
#-------------------------------------------------------------------------

"""    
class RoutineValidatorUT:
    """ 
    #-------------------------------------------------------------------------
    # class method to prepare a logging instance with standard ready ---------
    #---------------- @author: Leyner Bejarano (labejara) --------------------
    # inputs:
    #       - cls: implicit, class
    # output:
    #       vLogger : logging object
    # usage:
    #      vLogger = routineValidatorUT.fn_prepare_logging()
    #-------------------------------------------------------------------------
    """
    @classmethod
    def fn_prepare_logging(cls):
        vLogProperties = {'logger.name':'routineValidator',
                    'log.date.format':'%Y-%m-%d %H:%M:%S',
                    'log.format':'%(asctime)s - [%(levelname)s] - %(message)s',
                    'log.file.name':'logs/routineValidator_{}.log'.format(time.strftime('%Y%m%d')),
                    'log.file.max.size.bytes':'5242880',
                    'log.file.max.backup.count':'10000',
                    'log.file.encoding':'utf-8',
                    'log.file.delay.seconds':'5',
                    'logger.file.level':'FlowModule.LOG_LEVEL_DEBUG',
                    'logger.level':'FlowModule.LOG_LEVEL_DEBUG'}
        vLogger = FlowModule.fn_get_logger_module(flowName=vLogProperties['logger.name'], properties=vLogProperties)
        FlowModule.vLogger = vLogger
        FlowModule.fn_add_logger_file_handler(vLogProperties)
        FlowModule.fn_manage_log('''########################################################################################################''', vLevel=FlowModule.LOG_LEVEL_INFO)
        FlowModule.fn_manage_log('''############################################## NUEVA EJECUCION #########################################''', vLevel=FlowModule.LOG_LEVEL_INFO)
        FlowModule.fn_manage_log('''########################################################################################################''', vLevel=FlowModule.LOG_LEVEL_INFO)
        return vLogger
    """
    #-------------------------------------------------------------------------
    # class method to prepare a logging instance with standard ready --------- 
    #---------------- @author: Leyner Bejarano (labejara) --------------------
    # inputs:
    #       - cls: implicit, class
    # output:
    #       vLogger : logging object
    # usage:
    #      vLogger = routineValidatorUT.fn_prepare_logging()
    #-------------------------------------------------------------------------
    """
    @classmethod
    def fn_write_log(cls, logger, msg, logType, name):
            vMessage = "["+ name + "] " + ": " + msg
            if logType == logging.ERROR:
                logger.error(vMessage)
            elif logType == logging.WARNING:
                logger.warning(vMessage)
            elif logType == logging.INFO:
                logger.info(vMessage)
            elif logType == logging.CRITICAL:
                logger.critical(vMessage)
            elif logType == logging.DEBUG:
                logger.debug(vMessage)
            else:
                raise RuntimeError('Error al tratar de escribir en el log, nivel no identificado')
            return True
"""
#-------------------------------------------------------------------------
#----------------------------- Arguments parser --------------------------
#---------------- @author: Leyner Bejarano (labejara) --------------------
# components:
#           - Constants
#           - class methods
# usage:
#       vArguments = ArgParser.fn_get_args()
#-------------------------------------------------------------------------
"""
class ArgParser:
    MODULE_DESCRIPTION = "Programa para la deteccion de consultas con malas practicas\
         en los archivos .sql de las rutinas"
    MODULE_VERSION = "1.0"
    MODULE_EPILOG = "Equipo LZ"
    PROPERTIES_PATH = "Ruta al archivo de propiedades"
    ROUTINE_PATH = "Ruta a la carpeta con la rutina"
    ROUTINE_NAME = "Nombre de la  rutina"
    @classmethod
    def fn_get_args(cls):
        parser = argparse.ArgumentParser(description = cls.MODULE_DESCRIPTION, \
            epilog = cls.MODULE_EPILOG, version = cls.MODULE_VERSION)
        parser.add_argument('--properties-path', '-p', help = cls.PROPERTIES_PATH, \
            type = str, dest = 'vPropertiesPath', required = True)
        parser.add_argument('--routine-path', '-r', help = cls.ROUTINE_PATH, \
            type = str, dest = 'vRoutinePath', required = True)
        parser.add_argument('--routine-name', '-n', help = cls.ROUTINE_NAME, \
            type = str, dest = 'vRoutineName', required = True)
        arguments = parser.parse_args()
        return arguments
