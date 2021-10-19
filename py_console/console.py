import os
import datetime
from dataclasses import dataclass

import colorama

from py_console.definitions.console import ELogTypes


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
    __logDict:{int: ColoredLog} = {}
    settings = ConsoleSettings()


    def __init__(self):
        colorama.init(autoreset=False)

    # region Settings
    def setShowTimeDefault(self, doShowTime:bool):
        self.settings.showTime = doShowTime
    def setTimeFormat(self, timeFormat:str):
        self.settings.timeFormat = timeFormat
    # endregion

    # region Console Functions
    def clearScreen(self):
        """ PyCharm: tick box in run options: 'Emulate terminal in output console' to True """
        _ = os.system('cls||clear')
        print("", end="\r")
        pass
    # endregion Console Functions

    def __createConsoleRecord(self, type:ELogTypes, message:str, severe:bool, showTime:bool, textColor:str, bgColor:str):
        return ColoredLog(
            type=type,
            message=message,
            severe=severe,
            showTime=showTime or self.settings.showTime if (showTime == None) else showTime,
            timeFormat=self.settings.timeFormat,
            textColor=textColor,
            bgColor=bgColor
        )

    # region Printing lines
    def log(self, *message:str, severe:bool=False, showTime:bool=None):
        message = " ".join([str(m) for m in message])
        cr = self.__create_line(logType=ELogTypes.log, message=f'{message}', severe=severe, showTime=showTime)
        print(cr)
    def warn(self, *message:str, severe:bool=False, showTime:bool=None):
        message = " ".join([str(m) for m in message])
        cr = self.__create_line(logType=ELogTypes.warn, message=f'{message}', severe=severe, showTime=showTime)
        print(cr)
    def error(self, *message:str, severe:bool=False, showTime:bool=None):
        message = " ".join([str(m) for m in message])
        cr = self.__create_line(logType=ELogTypes.error, message=f'{message}', severe=severe, showTime=showTime)
        print(cr)
    def success(self, *message:str, severe:bool=False, showTime:bool=None):
        message = " ".join([str(m) for m in message])
        cr = self.__create_line(logType=ELogTypes.success, message=f'{message}', severe=severe, showTime=showTime)
        print(cr)
    def info(self, *message:str, severe:bool=False, showTime:bool=None):
        message = " ".join([str(m) for m in message])
        cr = self.__create_line(logType=ELogTypes.info, message=f'{message}', severe=severe, showTime=showTime)
        print(cr)
    def __create_line(self, logType:ELogTypes, message:str, severe:bool, showTime:bool):
        cr = self.__createConsoleRecord(
            type=logType,
            message=message, severe=severe,
            showTime=showTime,
            textColor=getDefaultTextColor(logType=logType, isSevere=severe),
            bgColor=getDefaultBgColor(logType=logType, isSevere=severe)
        )
        if (self.settings.keepHistory):
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

console_instance.settings.keepHistory = True
console_instance.success('tests', severe=True)
console_instance.warn('tests', 2, 'jo', 'tests', severe=True)
console_instance.error('tests', 2, 'jo', 'tests', severe=True)
console_instance.info('tests', 2, 'jo', 'tests', severe=True)
console_instance.log('tests', 2, 'jo', 'tests', severe=True)

console_instance.settings.showTime = True

console_instance.refresh_console()

