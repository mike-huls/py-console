import os
import datetime
import subprocess

import colorama

from enum import Enum

class ELogTypes(Enum):
    log = 'log'
    warn = 'warn'
    error = 'error'
    success = 'success'
    info = 'info'

class ConsoleRecord:

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



class Console:

    __reset: str = colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL # '\x1b[0m'
    __defaultShowTime:bool = True
    __defaultStyle:colorama.Style = colorama.Style.NORMAL
    __timeFormat:str = '%H:%M:%S'

    __logDict:{int: ConsoleRecord} = {}
    __keepHistory:bool = False

    def __init__(self):
        colorama.init(autoreset=False)

    # region Settings
    def setShowTimeDefault(self, doShowTime:bool):
        self.__defaultShowTime = doShowTime
    def setStyleDefault(self, defaultStyle:colorama.Style):
        self.__defaultStyle = defaultStyle
    def setTimeFormat(self, timeFormat:str):
        self.__timeFormat = timeFormat
    def setKeepHistory(self, doKeepHistory:bool):
        self.__keepHistory = doKeepHistory
    # endregion

    # region Console Functions
    def clearScreen(self):
        """ PyCharm: tick box in run options: 'Emulate terminal in output console' to True """
        # _ = subprocess.call('CLS' if os.name == 'nt' else 'clear', shell=True)
        # _ = os.system('cls' if os.name == 'nt' else 'clear')
        # print(chr(27) + "[2J")
        _ = os.system('cls||clear')
        print("", end="\r")
        pass
    # endregion Console Functions

    def __createConsoleRecord(self, type:ELogTypes, message:str, severe:bool, showTime:bool, textColor:str, bgColor:str):
        return ConsoleRecord(
            type=type,
            message=message,
            severe=severe,
            showTime=showTime or self.__defaultShowTime if (showTime == None) else showTime,
            timeFormat=self.__timeFormat,
            textColor=textColor,
            bgColor=bgColor
        )

    # region Printing lines
    def log(self, *message:str, severe:bool=False, showTime:bool=None):
        cr = self.__create_line(logType=ELogTypes.log, message=f'{" ".join(message)}', severe=severe, showTime=showTime)
        print(cr)
    def warn(self, *message:str, severe:bool=False, showTime:bool=None):
        cr = self.__create_line(logType=ELogTypes.warn, message=f'{" ".join(message)}', severe=severe, showTime=showTime)
        print(cr)
    def error(self, *message:str, severe:bool=False, showTime:bool=None):
        cr = self.__create_line(logType=ELogTypes.error, message=f'{" ".join(message)}', severe=severe, showTime=showTime)
        print(cr)
    def success(self, *message:str, severe:bool=False, showTime:bool=None):
        cr = self.__create_line(logType=ELogTypes.success, message=f'{" ".join(message)}', severe=severe, showTime=showTime)
        print(cr)
    def info(self, *message:str, severe:bool=False, showTime:bool=None):
        cr = self.__create_line(logType=ELogTypes.info, message=f'{" ".join(message)}', severe=severe, showTime=showTime)
        print(cr)
    def __create_line(self, logType:ELogTypes, message:str, severe:bool, showTime:bool):
        cr = self.__createConsoleRecord(
            type=logType,
            message=message, severe=severe,
            showTime=showTime,
            textColor=getDefaultTextColor(logType=logType, isSevere=severe),
            bgColor=getDefaultBgColor(logType=logType, isSevere=severe)
        )
        if (self.__keepHistory):
            self.__logDict[id(cr)] = cr
        return cr
    # endregion

    def highlight(self, message:str, bgColor:str=colorama.Back.YELLOW, textColor:str=colorama.Fore.BLACK):
        cr = self.__createConsoleRecord(
            type=ELogTypes.info.value,
            message=message, severe=False,
            showTime=False,
            textColor=textColor, bgColor=bgColor
        )
        return cr.__str__()

    def showHistory(self):
        for _id, cr in self.__logDict.items():
            print(cr)
    def refresh_console(self):
        """ Clears screen and prints history anew """
        self.clearScreen()
        self.showHistory()


console_instance = Console()

def aaa(*var, doeIets:bool):
    print(var)
    print(doeIets)
    print("____")

if __name__ == "__main__":
    aaa('test', 'jo', 'test', doeIets=True)
