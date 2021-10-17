import datetime
import colorama


class Console:

    __reset: str = colorama.Fore.RESET + colorama.Back.RESET  # '\x1b[0m'
    __defaultShowTime:bool = True
    __defaultStyle:colorama.Style = colorama.Style.NORMAL
    __timeFormat:str = '%H:%M:%S'

    def __init__(self):
        colorama.init(autoreset=False)
    def setShowTimeDefault(self, doShowTime:bool):
        self.__defaultShowTime = doShowTime
    def setStyleDefault(self, defaultStyle:colorama.Style):
        self.__defaultStyle = defaultStyle
    def setTimeFormat(self, timeFormat:str):
        self.__timeFormat = timeFormat

    def log(self, message:str, severe:bool=False, showTime:bool=None):
        bg = colorama.Back.BLACK if severe else ''
        fg = colorama.Fore.WHITE if severe else ''
        self.__print(fg=fg, bg=bg, showTime=showTime, msg=message)
    def warn(self, message:str, severe:bool=False, showTime:bool=None):
        bg = colorama.Back.YELLOW if severe else ''
        fg = colorama.Fore.BLACK if severe else colorama.Fore.YELLOW
        self.__print(fg=fg, bg=bg, showTime=showTime, msg=message)
    def error(self, message:str, severe:bool=False, showTime:bool=None):
        bg = colorama.Back.RED if severe else ''
        fg = colorama.Fore.BLACK if severe else colorama.Fore.RED
        self.__print(fg=fg, bg=bg, showTime=showTime, msg=message)
    def success(self, message:str, severe:bool=False, showTime:bool=None):
        bg = colorama.Back.GREEN if severe else ''
        fg = colorama.Fore.BLACK if severe else colorama.Fore.GREEN
        self.__print(fg=fg, bg=bg, showTime=showTime, msg=message)
    def info(self, message:str, severe:bool=False, showTime:bool=None):
        bg = colorama.Back.BLUE if severe else ''
        fg = colorama.Fore.BLACK if severe else colorama.Fore.BLUE
        self.__print(fg=fg, bg=bg, showTime=showTime, msg=message)

    def __getTime(self):
        return f"[{datetime.datetime.now().strftime(self.__timeFormat)}] "

    def get_string(self, fg:str, bg:str, msg:str, showTime:bool=None) -> str:
        # Take care of showing time: showTime if specified else __defaultShowTime
        if (showTime != None):
            theTime = self.__getTime() if (showTime) else ''
        else:
            theTime = self.__getTime() if (self.__defaultShowTime) else ''

        # Take care of highlighting in message
        if (self.__reset in msg):
            parts = msg.split(self.__reset)
            msg = f"{self.__reset}{fg}{bg}".join(parts)
        return f"{fg}{bg}{theTime}{msg}{self.__reset}"

    def __print(self, fg:str, bg:str, msg:str, showTime:bool=None):
        print(self.get_string(fg=fg, bg=bg, msg=msg, showTime=showTime))
    def highlight(self, msg:str, bgColor:str=colorama.Back.YELLOW, textColor:str= ''):
        return self.get_string(msg=msg, bg=bgColor, fg=textColor, showTime=False)

console_instance = Console()