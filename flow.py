# BigDataCompanyPY

import threading
import subprocess
import os
import sys
import types
import logging
import argparse
import time
from logging.handlers import RotatingFileHandler

class FlowModule:
    vLogger = None
    NOT_INT_GREAT_ZERO = "Revisar que sea entero y mayor a cero"
    BAD_FILE_PATH = "Revisa la ruta del archivo, recuerda debe ser un txt con paquete por linea"
    SUCCESS_END = "El administrador de hilos ha terminado"
    TOTAL_THREADS = "Total de hilos creados: "
    PACKAGE_FILE_PROBLEM = "No se pudo procesar el archivo de paquetes, revisar permisos"
    START_THREAD_ERROR = "Error al inicializar el hilo; "
    MODULE_DESCRIPTION = "Modulo para la ejecucion en paralelo de comandos bash"
    MODULE_VERSION = "1.0"
    MODULE_EPILOG = "Es posible usar los componentes por aparte, revisar flow.py"
    FILE_ARG_HELP = "Ruta del archivo con los comandos listos"
    THREADS_ARG_HELP = "Hilos que correran a la vez"
    THREAD_EXECUTING = "Thread %s Running"
    THREAD_STOPPED = "Thread %s Stopped"
    EXECUTE_MSG = "Comienza la ejecucion del flujo: "
    LOG_LEVEL_DEBUG = logging.DEBUG
    LOG_LEVEL_INFO = logging.INFO
    LOG_LEVEL_ERROR = logging.ERROR
    """
    #-------------------------------------------------------------------------
    #---- Function to initilialize and / or return a logger instance with ----
    #------------------------ standard format --------------------------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) ---------------------    
    # inputs:
    #       - moduleName, flowName: String with, String
    # output:
    #       - tuple with return code, stout and stderr from the subprocess 
    # usage:
    #       FlowModule.fn_get_logger_module()
    #-------------------------------------------------------------------------
    """
    @classmethod
    def fn_get_logger_module(cls, flowName=None, properties=None):
   	if FlowModule.vLogger is None:
            if flowName is None: FlowModule.vLogger = logging.getLogger(cls.__name__)
            else: FlowModule.vLogger = logging.getLogger(flowName)
            
            FlowModule.vLogger.setLevel(FlowModule.LOG_LEVEL_DEBUG)
            vLoggerHandler= logging.StreamHandler(sys.stdout)
            vFormatter = cls.fn_get_logger_formatter(properties)
            try: vLoggerHandler.setLevel(eval(properties['logger.level']))
            except: vLoggerHandler.setLevel(FlowModule.LOG_LEVEL_INFO)
            vLoggerHandler.setFormatter(vFormatter)
            FlowModule.vLogger.addHandler(vLoggerHandler)
        return FlowModule.vLogger 
    """
    #-------------------------------------------------------------------------
    #---- Function to add a file handler to the logger ----
    #------------------------ standard format --------------------------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) ---------------------    
    # inputs:
    #       - properties:dict()
                'logger.name':'Logger',
                'log.format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'log.date.format': '%Y %m %d %H:%M:%s',
                'log.file.name': 'logs/logger.log',
                'log.file.max.size.bytes': '5242880',
                'log.file.max.backup.count': '10000',
                'log.file.encoding': 'utf-8',
                'log.file.delay.seconds': '5'
    # output:
    #       - N/A
    # usage:
    #       FlowModule.fn_add_logger_file_handler(properties=None):
    #-------------------------------------------------------------------------
    """
    @classmethod
    def fn_add_logger_file_handler(cls, properties=None):
                if properties is None: properties = { 'logger.name':'Logger', 'log.format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s', 'log.date.format': '%Y %m %d %H:%M:%s', 'log.file.name': 'logs/logger.log', 'log.file.max.size.bytes': 5242880, 'log.file.max.backup.count': 10000, 'log.file.encoding': 'utf-8', 'log.file.delay.seconds': 5 }

                formatter = FlowModule.fn_get_logger_formatter(properties)
                rotatingFileHandler = RotatingFileHandler(properties['log.file.name'], maxBytes=int(properties['log.file.max.size.bytes']), backupCount=int(properties['log.file.max.backup.count']), encoding=properties['log.file.encoding'], delay=int(properties['log.file.delay.seconds']))
                rotatingFileHandler.setLevel(FlowModule.LOG_LEVEL_DEBUG)
                rotatingFileHandler.setFormatter(formatter)                
                FlowModule.vLogger.addHandler(rotatingFileHandler)
    """
    #-------------------------------------------------------------------------
    #---- Function to initilialize and / or return a logger formmatter with --
    #------------------------ standard format --------------------------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Daniel Restrepo (drhinca) ---------------------
    # inputs:
    #       - properties: { log.format, log.date.format }
    # output:
    #       - instance of logging.Formatter
    # usage:
    #       FlowModule.fn_get_logger_formatter(properties=None)
    #-------------------------------------------------------------------------
    """ 
    @classmethod
    def fn_get_logger_formatter(cls, properties=None):
          if properties is not None: 
             try: vFormatter = logging.Formatter(properties['log.format'], properties['log.date.format'])
             except: vFormatter = logging.Formatter(properties['log.format'])
          else: vFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
          
	  return vFormatter
    """
    #-------------------------------------------------------------------------
    #---- Function to print a log record from an existent logger or not ------
    #------------------------ standard format --------------------------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Daniel Restrepo (drhinca) ---------------------
    # inputs:
    #       - vMessage: String, vError: String (Default None)
    #       - vOption: String ("i": INFO, "e": ERROR, "d": DEBUG)
    # output:
    #       - None
    # usage:
    #       FlowModule.fn_manage_log(vMessage, vError, vOption=[i,e,d])
    #-------------------------------------------------------------------------
    """
    @classmethod
    def fn_manage_log(cls, vMessage, vError=None, vClassName=None, vLevel=LOG_LEVEL_INFO):
    	vMessage = vMessage if vError is None else "{}: {}".format(vMessage, vError)

	if FlowModule.vLogger is None:
		vMessage = vMessage if vClassName is None and not isinstance(vClassName, str) else "{} - {}".format(vClassName, vMessage)
		
		if vLevel == FlowModule.LOG_LEVEL_INFO: print("INFO {}".format(vMessage))
		elif vLevel == FlowModule.LOG_LEVEL_ERROR: print("ERROR {}".format(vMessage))
		elif vLevel == FlowModule.LOG_LEVEL_DEBUG: print("DEBUG {}".format(vMessage))
		else: raise ValueError("Unsupported logger option.")
	else:
		if vClassName is not None and isinstance(vClassName, str): 
            		childLogger = FlowModule.vLogger.getChild(vClassName)
	    		if vLevel == FlowModule.LOG_LEVEL_INFO: childLogger.info(vMessage)
            		elif vLevel == FlowModule.LOG_LEVEL_ERROR: childLogger.error(vMessage)
           		elif vLevel == FlowModule.LOG_LEVEL_DEBUG: childLogger.debug(vMessage)
            		else: raise ValueError("Unsupported logger option.")
        	else:
            		if vLevel == FlowModule.LOG_LEVEL_INFO: FlowModule.vLogger.info(vMessage)
            		elif vLevel == FlowModule.LOG_LEVEL_ERROR: FlowModule.vLogger.error(vMessage)
            		elif vLevel == FlowModule.LOG_LEVEL_DEBUG: FlowModule.vLogger.debug(vMessage)
            		else: raise ValueError("Unsupported logger option.")
		
    """
    #-------------------------------------------------------------------------
    #------------ Function to write in logger based on status code -----------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) -----------------------    
    # inputs:
    #       - self FlowModule
    #       - message to write
    #       - statusCode 0 for info any other for error
    # output:
    #       - None
    # usage:
    #       vInstanceFlowThreadsManager.fn_run()
    #-------------------------------------------------------------------------
    """
    @classmethod
    def fn_write_logger(cls,message,statusCode):
            vLogger = FlowModule.fn_get_logger_module()
            if statusCode == 0: vLogger.info(message)
            else: vLogger.error(message)
            return None
    """
    #-------------------------------------------------------------------------
    #--------------- Function to get commands from list or file --------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) -----------------------
    # inputs:
    #       - self
    # output:
    #       - Commands list
    # usage:
    #      FlowModule.fn_create_commands_packages_from_file(packageNamesFile,
    #           packageType,parametersList)
    #-------------------------------------------------------------------------
    """
    @classmethod
    def fn_create_commands_packages_from_file(cls,packageNamesFile,packageType,parametersList):
        vCommandsList=[]
        with open(packageNamesFile, "r") as vFile:
            vLine = vFile.readline()
            while vLine:
                vLine= vLine.rstrip()
                vLine = "./"+vLine
                vLine += "-"+packageType+".sh"
                for vParameter in parametersList:
                    vLine +=" "+vParameter
                vCommandsList.append(vLine)
                vLine = vFile.readline()
        return vCommandsList
    """
    #-------------------------------------------------------------------------
    #--------------- Function to get commands from list or file --------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) -----------------------
    # inputs:
    #       - self
    # output:
    #       - Commands list
    # usage:
    #       FlowModule.fn_get_prepared_commands_from_file(commandsFilePath)
    #-------------------------------------------------------------------------
    """
    @classmethod
    def fn_get_prepared_commands_from_file(cls,commandsSource):
        vCommandsList=[]
        with open(commandsSource, "r") as vFile:
            vLine = vFile.readline()
            while vLine:
                vLine= vLine.rstrip()
                vCommandsList.append(vLine)
                vLine = str(vFile.readline())
        return vCommandsList

class FlowSubProcess:
    def __init__(self,newCommand):
        self.vCommandToExecute = newCommand
    
    """
    #-------------------------------------------------------------------------
    #----- Function to execute a subprocess with shell features --------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) -----------------------
    # inputs:
    #       - 
    # output:
    #       - tuple with return code, stout and stderr from the subprocess 
    # usage:
    #       vInstanceflowSubProcess.fn_execute_command()
    #-------------------------------------------------------------------------
    """
    def fn_execute_command(self):
        try:   
            vSubprocess = subprocess.Popen(self.vCommandToExecute, shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
            vStdOutputs = vSubprocess.communicate()
            return (vSubprocess.returncode,str(vStdOutputs[0]),str(vStdOutputs[1]))
        except:
            return (1,"",sys.exc_info)

class FlowThread(threading.Thread):
    def __init__(self,flowSubProcess, flowName = None, printOut=False, printErr=False):
        threading.Thread.__init__(self)
        if flowName is not None: self.setName(flowName)
        else: self.setName("Thread")

        self.flowSubProcess = flowSubProcess
        self.isChecked=False
        self.__outPut=None

        self.__print_out = printOut
        self.__print_err = printErr

    """
    #-------------------------------------------------------------------------
    #--------------- Overriden run function for Thread -----------------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) -----------------------
    # inputs:
    #       - self: FlowThread
    # output:
    #       - None
    # usage:
    #       vInstanceFlowThreadsManager.run() 
    #       vInstanceflowThread.start() for thread processing 
    #-------------------------------------------------------------------------
    """
    def run(self):
        vTuple = self.flowSubProcess.fn_execute_command()
        outMessage = "%s \n\t-- FinishStatus: %s" % (self.flowSubProcess.vCommandToExecute, str(vTuple[0]))
        if self.__print_out: outMessage = outMessage + "\n\t-- Out: %s" % (str(vTuple[1]))
       
        if self.__print_err: outMessage = outMessage + "\n\t-- Err: %s\n" % (str(vTuple[2]))
        FlowModule.fn_write_logger(outMessage, vTuple[0])
        self.__outPut = vTuple

    """
    #-------------------------------------------------------------------------
    #--------------- Overriden run function for Thread -----------------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Daniel Restrepo (drhinca) -----------------------
    # inputs:
    #       - self: FlowThread
    # output:
    #       - self.__outPut
    # usage:
    #       vInstanceFlowThreadsManager.join() Lock the Thread until done 
    #-------------------------------------------------------------------------
    """ 
    def join(self):
        super(FlowThread, self).join()
        if self.isAlive(): FlowModule.fn_write_logger(FlowModule.THREAD_EXECUTING % (str(self.getName())),0)
        else: FlowModule.fn_write_logger(FlowModule.THREAD_STOPPED  % (str(self.getName())),0)
        return self.__outPut


class FlowThreadsManager:
    """
    #-------------------------------------------------------------------------
    #----- Function to create and validates threads manager parameter --------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) -----------------------
    # inputs:
    #       - commandsSource path to file or list with commands
    #           commands to run
    #       - parallelExecutions int of parallel package executions 
    # output:
    #       - FlowThreadManager object validated 
    # usage:
    #       FlowThreadManager(commandsSource, parallelExecutions)
    #-------------------------------------------------------------------------
    """
    def __init__(self, commandsList, parallelExecutions, logger=None, printOut=False, printErr=False, sleepTime=0):
        self.__print_out = printOut
        self.__print_err = printErr
	self.__sleep_time = sleepTime
        if logger is not None: self.vLogger = logger  
        else: self.vLogger = FlowModule.fn_get_logger_module()

        self.threadOuPutsList = list()
        self.__customHandler = None

        if type (parallelExecutions) is not types.IntType or parallelExecutions <= 0:
            self.vLogger.error(FlowModule.NOT_INT_GREAT_ZERO)
            sys.exit(1)

        if isinstance(commandsList, types.ListType): 
            self.isDictionary = False

        elif isinstance(commandsList, types.DictionaryType):
            self.isDictionary = True
        else:
            self.vLogger.error(FlowModule.BAD_FILE_PATH)
            sys.exit(1)
          
        self.vParallelExecutions = parallelExecutions
        self.vCommandsList= commandsList
        
    def add_hadler(self, handler=None):
        self.__customHandler = handler

    """
    #-------------------------------------------------------------------------
    #--- function to create threads with a FlowSubProcess instance ---
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) -----------------------
    # inputs:
    #       - commandsList: string list with commands  
    # output:
    #       - FlowMyThread list with the created threads  
    # usage:
    #       vInstanceFlowThreadsManager.fn_run_in_threads(commandsList)
    #-------------------------------------------------------------------------
    """

    def fn_run_in_threads(self, commandsList):
        vThreadsList = []
        if not self.isDictionary:
            commandsList = dict(zip(map(lambda x: str(x), range(0, len(commandsList))), commandsList))

        for i in commandsList.keys():
            if self.vParallelExecutions <= 0:
                vCheck= True
                while vCheck:
                    for j in range(0,len(vThreadsList)):
                        if not vThreadsList[j].is_alive() and not vThreadsList[j].isChecked:
                            self.vParallelExecutions = self.vParallelExecutions + 1
                            vCheck=False
                            vThreadsList[j].isChecked=True
            vSubprocess = FlowSubProcess(commandsList[i])
            vThread = FlowThread(vSubprocess, flowName=i, printOut=self.__print_out, printErr=self.__print_err)
            if self.vLogger is not None: self.vLogger.info(FlowModule.EXECUTE_MSG + i + "\n")
            try:
                time.sleep(self.__sleep_time)
                vThread.start()
            except Exception as ex:
                self.vLogger.error(FlowModule.START_THREAD_ERROR+vThread.flowSubProcess.\
                    vCommandToExecute)
                self.vLogger.error(str(ex))
            vThreadsList.append(vThread)
            self.vParallelExecutions = self.vParallelExecutions - 1

            

        return vThreadsList
    """
    #-------------------------------------------------------------------------
    #--------------- Main function to run the commands provided --------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) -----------------------
    # inputs:
    #       - self: FlowThreadsManager
    # output:
    #       - None
    # usage:
    #       vInstanceFlowThreadsManager.fn_han()
    #-------------------------------------------------------------------------
    """
    def __fn_handle_exit(self):
        if self.__customHandler is not None: self.__customHandler(self.vOutput)

        try:
              if self.vOutput[0] == 0: self.vLogger.info("{0}: SUCCEEDED.".format(self.threadName))
              else: self.vLogger.info("{0}: FAILED.".format(self.threadName))
        except: pass

        self.threadOuPutsList.append([self.threadName, self.vOutput])

    """
    #-------------------------------------------------------------------------
    #--------------- Main function to run the commands provided --------------
    #---------------- @author: Sebastian Lopez (slvalen) ---------------------
    #---------------- @author: Mateo Alvarez (magarci) -----------------------
    # inputs:
    #       - self: FlowThreadsManager
    # output:
    #       - None
    # usage:
    #       vInstanceFlowThreadsManager.fn_run()
    #-------------------------------------------------------------------------
    """
    def fn_run(self):
        vThreadsList = self.fn_run_in_threads(self.vCommandsList)        
        for i in range(0,len(vThreadsList)):
            self.threadName = vThreadsList[i].getName()
            self.vOutput = vThreadsList[i].join() 
            self.__fn_handle_exit()
        self.vLogger.info(FlowModule.TOTAL_THREADS + str(len(vThreadsList)))
        self.vLogger.info(FlowModule.SUCCESS_END)
        return None
    
    
if __name__ == '__main__':
    #Commands validation
    parser = argparse.ArgumentParser(description = FlowModule.MODULE_DESCRIPTION,\
    epilog = FlowModule.MODULE_EPILOG, version = FlowModule.MODULE_VERSION)
    parser.add_argument('--commands-file', '-f', help = FlowModule.FILE_ARG_HELP,\
        type = str, dest = 'vFilePath', required = True)
    parser.add_argument('--threads', '-t', help = FlowModule.THREADS_ARG_HELP,\
        type = int, dest = 'vThreadsAtTime', required = True)
    arguments = parser.parse_args()
    #run from a commands file
    vCommandsList = FlowModule.fn_get_prepared_commands_from_file(arguments.vFilePath)
    flowThreadsManager = FlowThreadsManager(vCommandsList,arguments.vThreadsAtTime)
    flowThreadsManager.fn_run()

    #Example running with python
    # vCommandsEval = ["notepad","Notepad","echo Hola Mundo","Mundo","mspaint"]
    # flowThreadsManager = FlowThreadsManager(vCommandsEval,2)
    # flowThreadsManager.fn_run()

    #Example with a package file as input to build commands
    # vListTemp = []
    # vListTemp.append(sys.argv[3])
    # vListTemp.append(sys.argv[4])
    # vCommandsList = []
    # try:
    #     vCommandsList = FlowModule.fn_create_commands_packages_from_file(sys.argv[1],sys.argv[2],vListTemp)
    # except Exception as ex:
    #     print FlowModule.BAD_FILE_PATH
    #     sys.exit(1)
    # else:
    # Show commands
    #     print vCommandsList
    #     flowThreadsManager = FlowThreadsManager(vCommandsList,int(sys.argv[5]))
    #     flowThreadsManager.fn_run()
