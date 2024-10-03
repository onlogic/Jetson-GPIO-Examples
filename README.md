# Utilizing GPIO for Aetina Jetson systems

This guide will walk you through utilizing GPIO pins on the 15-pin header located on the rear of your Jetson device with the [libgpiod C library](https://github.com/brgl/libgpiod), specifically the command line interface and official python binding to demonstrate key concepts. This demo was created using an Orin NX running Jetpack 6.0 [L4T 36.3].
> [!WARNING]
> Any Python Code in this repository is purely for demonstration and testing purposes. Please ensure to visit the libgpiod repository for more info on [python-based bindings](https://github.com/brgl/libgpiod/tree/master/bindings/python). DO NOT USE FOR SAFETY CRITICAL APPLICATIONS.

## What is libgpiod? <br/>
libgpiod is a C library designed to interact with linux GPIO devices. Since linux 4.8, the sysfs interface has been depricated and it is recommended to use charcter devices instead. This also means that the CLI tool shown below was also depricated. This demo will walk through some basic demos to show functionality interacting with the GPIO.

## Basic Installation Steps <br/>
The old version of gpiod(v1.5.4) was depricated and the below sample code has been based on the currently supported release, You will need at least v2.0.2. Depending on your installed version of Jetpack, you likely have a depricated version of libgpiod installed for system functions. We want to make sure the user calls upon a recent version:
- Open a terminal session
- First we should ensure are system is up to date ``` sudo apt-get upgrade ```
- libgpiod depends on ``` python3-dev``` , this should already been installed, but just in case we can run ```sudo apt install python3-dev```
- Next we can install gpiod. ```pip install gpiod```. Running ```pip list --user``` should show the package.
  - Ensure this installs a version later than 2.0.2.
  - If you see 1.5.4 being installed, you can run ```pip uninstall gpiod``` and then ```pip install gpiod==``` to check if you can install a recent version.
  - If you encounter an error that the package is not available, You should upgrade your Jetson to a newer version of Jetpack before continuing. Reference our [Jetpack 6 upgrade guide](https://github.com/onlogic/Updating-to-Jetpack-6-for-Aetina-Jetson.git) for more information.

## Jetson GPIO Pin Basics <br/>

Before we dive into samples, let's take a brief look at the GPIO pins available. Each Aetina Jetson system has GPIO located the rear of the system. For all systems there is a DB-15 connector multi-purpose I/O, which is where are GPIO pins are. You can reference the system manuals for PIN addresses, but for simplicity they are listed below.
  - [Nano/NX Manual](https://www.dropbox.com/scl/fi/o4rogjf4r6nldqs6ow7e8/Aetina_AIE-PO22_32_PN32_42_user-manual.pdf?rlkey=d85bauvq4isimlzmu8hwtrq8r&e=2&dl=0)
  - [AGX Manual](https://www.dropbox.com/scl/fi/1kd6sd7g5kd8r4elcy8z9/Aetina_AIE-PX11_12_21_22_user-manual.pdf?rlkey=qvd8hx4iviah4kxvqsovmy9rs&e=1&dl=0)

**Nano/NX GPIO Pins**
| Physical Pin | GPIO Name | Linux Pin Name| gpiochip0 line # |
| --- | --- | --- | --- |
| 1 | GPIO01 | PQ.05 | 105 |
| 2 | GPIO11 | PQ.06 | 106 |
| 3 | GPIO12 | PN.01| 85
| 4 | GPIO13 | PH.00 | 43 |
| 5 | GPIO05 | PZ.07 | 137 |

**AGX GPIO Pins**
| Physical Pin | GPIO Name | Linux Pin Name |
| --- | --- | --- |
| 1 | GPIO17 | PP.04 |
| 2 | GPIO11 | PAC.05 |
| 3 | PWM01 | PR.00 |
| 4 | GPIO27 | PN.01 |
| 5 | GPIO35 | PH.00 |

We will use NX GPIO01 for the following examples. We can call upon these pins to set an output (High/Active = 3.3V) (Low/Inactive = 0V) or set as an input.

## Libgpiod Identifying Pins - Python (Current)
Since we can no longer user the CLI tool to gather information on our pins. We should run the following if we want to use lines or identify chips.
```python
import gpiod

with gpiod.Chip("/dev/gpiochip0") as chip:
    info = chip.get_info()
    print(f"{info.name} [{info.label}] ({info.num_lines} lines)")
```
This assumes you already know which chip the GPIO is on. If you'd like to check if a chip exists you can use the following, replacing x with the chip you'd like to identify.
```python
gpiod.is_gpiochip_device("/dev/gpiochipX")
```

## Libgpiod Identifying Pins - Command Line (Depricated)
To interface with GPIO pins we need to know the chip it is on and then the line (We can use either the GPIO Name (ex. PQ.05) or the chip line (105) in most cases). Reminder: This requires the depricated version of the package. You can install it with ```python sudo apt-get install gpiod```. Ensure your applications are calling on the user installed 2.0+ version or the below code examples will not work. <br/>
``` gpioinfo ``` will allow us to list all of the chips and their lines. Let's find the info we need for GPIO01. Here we can see that gpiochip0 contains our address. <br/>
![gpioinfo cli](/assets/gpioinfo1.png) <br/>
Scrolling down to PQ.05 shows us that corresponding line for chip gpiochip0 is 105. <br/>
![gpioinfo cli](/assets/gpioinfo2.png) <br/>

There are additional cli commmands avaiable such as ```gpioget``` and ```gpioset``` for temporarily reading and setting values. ```gpiomon``` which waits for edge events and ```gpionofity``` which waits for state changes. More info on usage can be found on the libgpiod readme.


## Libgpiod Python Sample Code
Let's breakdown a simple output script, based on official examples. The following uses line #, but remember we can also use the name shown above.
```python
import gpiod
import time
from gpiod.line import Direction, Value

LINE = 105

with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="basic-demo",
    config={
        LINE: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    },
) as request:
    while True:
        request.set_value(LINE, Value.ACTIVE)
        print("Active")
        time.sleep(10)
        request.set_value(LINE, Value.INACTIVE)
        print("Inactive")
        time.sleep(10)
        print("Complete")
```
An important note about gpiod, quitting forcefully will cause the pin to hang in the last known state. If you try to immediately run code against the same pin from the same terminal window after force quiting you will recieve an error "IOError: [Errno 16] Device or resource busy". With v2.0.2+ releasing the pin is as simple as opening up a new terminal window. Always design a way for your code to exit gracefully if using GPIO pins.

```python
# First we are importing the necessary packages
import gpiod 
import time

# In this example we will use:
# Direction, which means is it an input or an output
# Value which is the high or low state for output pins.
from gpiod.line import Direction, Value

#Here we will set a global variable for the line we want to use.
LINE = 105
```
<br/>

```python
# Here we are defining our request for the line.
# We first define the target chip, remember line 105 is contained in gpiochip0
# Creating a GPIO virtual device (consumer) to request the GPIO
# The creating a configuration for what we want are line to do. setting the direction as output and the initial value as Active (High)
with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="basic-demo",
    config={
        LINE: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    },
```
<br/>

```python
# Now we can call our request
) as request: 
    while True:
        #We are calling request to set the value, of LINE 105, and set the Value to High
        request.set_value(LINE, Value.ACTIVE)
        print("Active")
        time.sleep(10)
        #Here we are doing the same call as above, but this time we are setting teh Value to Low
        request.set_value(LINE, Value.INACTIVE)
        print("Inactive")
        time.sleep(10)
        print("Complete")
```
Using a multimeter, we can check that the code is working correctly. During active we should see 3.3V, whereas during inactive we should see 0V.
Now you see how we can how we can create a basic output example, let's look at some other requests. If we wanted to reconfigure the direction of a line from an output to an input, we could do so with the following:

```python
request.reconfigure_lines(
            config={line_offset: gpiod.LineSettings(
                    direction=Direction.INPUT
                )
            }
        )
```
If we wanted to then read the value of the input we could call:

```python
as request:
        value = request.get_value(LINE)
        print("{}={}".format(LINE, value))
```
These are just a few examples of what's possible with libgpiod. For further examples, check out the official [libgpiod examples repository](https://github.com/brgl/libgpiod/tree/master/bindings/python/examples).





