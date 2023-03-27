import re
import string
from logging import handlers
import logging
import os
import datetime
from dataclasses import dataclass

import colorama

from src.py_console.definitions import ELogTypes


class ColoredLog:

    type:ELogTypes
    message:str
    timestamp:datetime.datetime
    severe:bool
    showTime:bool
    timeFormat:str
    textColor:colorama.Fore
    bgColor:colorama.Back
    style:colorama.Style
    __reset: str = colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL # '\x1b[0m'


    def __init__(self, type:ELogTypes, message:str, severe:bool, showTime:bool, timeFormat:str, textColor:colorama.Fore, bgColor:colorama.Back):
        self.type = type
        self.message = message
        self.timestamp = datetime.datetime.now()
        self.severe = severe
        self.showTime = showTime
        self.timeFormat = timeFormat
        self.textColor = textColor #if (textColor != None) else self.__getDefaultTextColor()
        self.bgColor = bgColor #if (bgColor != None) else self.__getDefaultBgColor()
        self.style = colorama.Style.NORMAL

    def __str__(self):
        _timestamp = f"[{self.timestamp.strftime(self.timeFormat)}] " if (self.showTime) else ''
        msg = self.message
        if (self.__reset in self.message):
            parts = self.message.split(self.__reset)
            msg = f"{self.__reset}{self.style}{self.textColor}{self.bgColor}".join(parts)
        return f"{self.style}{self.textColor}{self.bgColor}{_timestamp}{msg}{self.__reset}"


def getDefaultTextColor(logType:ELogTypes, isSevere:bool):
    if (logType == ELogTypes.log):        return colorama.Fore.WHITE if (isSevere) else ''
    elif (logType == ELogTypes.warn):     return colorama.Fore.BLACK if (isSevere) else colorama.Fore.YELLOW
    elif (logType == ELogTypes.error):    return colorama.Fore.BLACK if (isSevere) else colorama.Fore.RED
    elif (logType == ELogTypes.success):  return colorama.Fore.BLACK if (isSevere) else colorama.Fore.GREEN
    elif (logType == ELogTypes.info):     return colorama.Fore.BLACK if (isSevere) else colorama.Fore.BLUE
def getDefaultBgColor(logType:ELogTypes, isSevere:bool):
    if (logType == ELogTypes.log):        return colorama.Back.BLACK if (isSevere) else ''
    elif (logType == ELogTypes.warn):     return colorama.Back.YELLOW if (isSevere) else ''
    elif (logType == ELogTypes.error):    return colorama.Back.RED if (isSevere) else ''
    elif (logType == ELogTypes.success):  return colorama.Back.GREEN if (isSevere) else ''
    elif (logType == ELogTypes.info):     return colorama.Back.BLUE if (isSevere) else ''

@dataclass()
class ConsoleSettings:
    showTime:bool = True
    keepHistory:bool = False
    timeFormat:str = '%H:%M:%S'


class Console:

    __reset: str = colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL # '\x1b[0m'
    __log_history:{int: ColoredLog} = {}
    settings = ConsoleSettings()
    __logger:logging.Logger = None

    def __init__(self):
        colorama.init(autoreset=False)

    # region Settings
    def setShowTimeDefault(self, doShowTime:bool):
        self.settings.showTime = doShowTime
    def setTimeFormat(self, timeFormat:str):
        self.settings.timeFormat = timeFormat
    def setLoggingPath(self, path:str, when:str, interval:int, backup_count:int, encoding:str='utf=8', overwrite:bool=False):
        """ Logs out all printed statements to a file """
        logger = logging.getLogger(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        logger.setLevel(level=logging.DEBUG)
        # create console handler with a higher log level
        fh: handlers.TimedRotatingFileHandler = handlers.TimedRotatingFileHandler(
            filename=path,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding=encoding,
        )
        # Log everything
        fh.setLevel(logging.DEBUG)
        # Format the logs
        formatter = logging.Formatter('%(message)s')
        formatter.datefmt = "%H:%M:%S"
        fh.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        self.__logger = logger
    # endregion

    # region Console Functions
    def clearScreen(self):
        """ PyCharm: tick box in run options: 'Emulate terminal in output console' to True """
        _ = os.system('cls||clear')
        print("", end="\r")
        pass
    # endregion Console Functions


    # region Printing lines
    def log(self, *msg:str, severe:bool=False, showTime:bool=None):
        msg = " ".join([str(m) for m in msg])
        cr = self.__create_line(logType=ELogTypes.log, message=f'{msg}', severe=severe, showTime=showTime)
        self.__log_line(log=cr)
    def warn(self, *msg:str, severe:bool=False, showTime:bool=None):
        msg = " ".join([str(m) for m in msg])
        cr = self.__create_line(logType=ELogTypes.warn, message=f'{msg}', severe=severe, showTime=showTime)
        self.__log_line(log=cr)
    def error(self, *msg:str, severe:bool=False, showTime:bool=None):
        msg = " ".join([str(m) for m in msg])
        cr = self.__create_line(logType=ELogTypes.error, message=f'{msg}', severe=severe, showTime=showTime)
        self.__log_line(log=cr)
    def success(self, *msg:str, severe:bool=False, showTime:bool=None):
        msg = " ".join([str(m) for m in msg])
        cr = self.__create_line(logType=ELogTypes.success, message=f'{msg}', severe=severe, showTime=showTime)
        self.__log_line(log=cr)
    def info(self, *msg:str, severe:bool=False, showTime:bool=None):
        msg = " ".join([str(m) for m in msg])
        cr = self.__create_line(logType=ELogTypes.info, message=f'{msg}', severe=severe, showTime=showTime)
        self.__log_line(log=cr)
    def __create_line(self, logType:ELogTypes, message:str, severe:bool, showTime:bool) -> ColoredLog:
        cr = self.__createConsoleRecord(
            type=logType,
            message=message, severe=severe,
            showTime=showTime,
            textColor=getDefaultTextColor(logType=logType, isSevere=severe),
            bgColor=getDefaultBgColor(logType=logType, isSevere=severe)
        )
        if (self.settings.keepHistory):
            self.__log_history[id(cr)] = cr
        return cr
    def __log_line(self, log:ColoredLog):
        # Print out the log to console
        print(log)
        # Handle printing to the logfile


        if (self.__logger is not None):
            # Clean up the log message: remove all color characters
            printable = set(string.printable)
            _logmsg = "".join(filter(lambda x: x in printable, log.message))
            _logmsg = re.sub('\[\d{1,2}m', '', _logmsg)
            logmsg = f"{str(log.type.value).ljust(8)} {_logmsg}"

            # Format the message some more
            if (log.showTime):
                logmsg = f"{str(log.type.value).ljust(8)} {log.timestamp} - {_logmsg}"
            if (log.severe):
                logmsg = logmsg.upper()
            self.__logger.log(msg=logmsg, level=logging.DEBUG)
    # endregion

    def __createConsoleRecord(self, type:ELogTypes, message:str, severe:bool, showTime:bool, textColor:str, bgColor:str) -> ColoredLog:
        return ColoredLog(
            type=type,
            message=message,
            severe=severe,
            showTime=showTime or self.settings.showTime if (showTime == None) else showTime,
            timeFormat=self.settings.timeFormat,
            textColor=textColor,
            bgColor=bgColor
        )
    def highlight(self, message:str, bgColor:str=colorama.Back.YELLOW, textColor:str=colorama.Fore.BLACK):
        cr = self.__createConsoleRecord(
            type=ELogTypes.info.value,
            message=message, severe=False,
            showTime=False,
            textColor=textColor, bgColor=bgColor
        )
        return cr.__str__()

    def showHistory(self):
        cr: ColoredLog
        for _id, cr in self.__log_history.items():
            print(cr)
    def refresh_console(self):
        """ Clears screen and prints history anew """
        self.clearScreen()
        self.showHistory()



console_instance = Console()


