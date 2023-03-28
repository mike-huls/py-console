import unittest
from py_console import console
from py_console import textColor, bgColor


class TestExample(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_demo(self):
        """ Test example """

        console.settings.keepHistory = True
        # 1. Arrange
        console.setLoggingPath(
            path='test.log',
            when='d',
            interval=1,
            backup_count=1
        )


        # Specify console settings
        # Show time in console.log, console.warn etc by default?
        console.setShowTimeDefault(True)
        # Custom format for showing time (default H:M:S)
        # Here we've added miliseconds
        console.setTimeFormat(timeFormat='%H:%M:%S.%f')

        # normal logging
        console.log("log")
        console.warn("warn", severe=False)
        console.error("error", severe=False)
        console.success("success", severe=False)
        console.info("info", severe=False)

        print(" ")

        # Change time format back
        console.setTimeFormat(timeFormat='%H:%M:%S')

        # all of these colors also have the 'severe' option
        console.log("log severe", severe=True)
        console.warn("warn severe", severe=True)
        console.error("error severe", severe=True)
        console.success("success severe", severe=True)
        console.info("info severe", severe=True)

        print(" ")

        # Specifying showTime ignores the defaults
        console.warn('Not showing time', showTime=False)

        print(" ")

        # Logging with highlighted text
        console.log(f"Normal log with default {console.highlight('highlighted')} part")
        console.log(
            f"Normal log with a {console.highlight('FAIL', bgColor=bgColor.RED)} "
            f"and a {console.highlight('SUCCESS', bgColor=bgColor.GREEN)} part")
        console.log(
            f"Severe log with a {console.highlight('FAIL', bgColor=bgColor.RED, textColor=textColor.BLACK)} "
            f"and a {console.highlight('SUCCESS', bgColor=bgColor.GREEN, textColor=textColor.BLACK)} part", severe=True)
        console.log(f"Normal log with {console.highlight('highlighted red', bgColor=bgColor.RED)} part")
        console.info(f"normal info with {console.highlight('highlighted red text', textColor=textColor.RED)} part")
        console.warn(f"Normal warn with {console.highlight('only red text', textColor=textColor.RED, bgColor='')} part")
        console.error(f"Error text with custom {console.highlight('black-yellow', textColor=textColor.YELLOW, bgColor=bgColor.BLACK)} highlights")

        print("HIST")
        console.showHistory()




if __name__ == '__main__':
    unittest.main()
