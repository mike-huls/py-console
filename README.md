# Welcome to py-console
I've always liked the ease with which we can log colorfull warning, errors and messages using JavaScript in a webbrowser console.
This package allows you to do just that

## Installation
```commandline
pip install py-console
```

## Usage
Main features:
 - printing lines with colored text and/or text backgrounds
 - printing lines of which parts have colored text or text backgrounds

### Demo
```python
from py_console import console, bgColor, textColor

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

# Change time format back
console.setTimeFormat(timeFormat='%H:%M:%S')

# all of these colors also have the 'severe' option
console.log("log severe", severe=True)
console.warn("warn severe", severe=True)
console.error("error severe", severe=True)
console.success("success severe", severe=True)
console.info("info severe", severe=True)

# Specifying showTime ignores the defaults
console.warn('Not showing time', showTime=False)

# Logging with highlighted text
console.error(f"Regular error with {console.highlight('highlighted')} part")
console.error(f"Regular error with not {console.highlight('one')} but {console.highlight('two')} highlighted parts")
console.error(f"Severe error with {console.highlight('highlighted')} part", severe=True)
console.warn(f"Warning text with custom {console.highlight('red highlighted', textColor=textColor.RED)} part")
console.error(f"Error text with custom {console.highlight('white-blue', textColor=textColor.BLUE, bgColor=bgColor.RED)} part")
console.warn(f"Severe error text with custom {console.highlight('white-blue', textColor=textColor.WHITE, bgColor=bgColor.BLUE)} part", severe=True)
console.warn(f"Severe error text with custom {console.highlight('white-blue', textColor=textColor.BLUE, bgColor=bgColor.RED)} part", severe=True)
```

## Output:  

![output_example](https://raw.githubusercontent.com/mike-huls/py-console/main/images/outputs.png)

### Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License
[MIT](https://choosealicense.com/licenses/mit/)