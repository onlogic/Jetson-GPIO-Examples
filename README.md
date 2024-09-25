# Utilizing GPIO for Aetina Jetson systems

This guide will walk you through utilizing GPIO pins on the 15-pin header located on the rear of your Jetson device with the [libgpiod C library](https://github.com/brgl/libgpiod), specifically the command line interface and simple Python sample code to demonstrate key concepts. This demo was created using an Orin NX running Jetpack 6.0 [L4T 36.3].
> [!WARNING]
> Any Python Code in this repository is purely for demonstration and testing purposes, and is not for production purposes. Please ensure to visit the libgpiod repository for more info on [python-based bindings](https://github.com/brgl/libgpiod/tree/master/bindings/python).

## What is libgpiod? <br/>
libgpiod is a C library designed to interact with linux GPIO devices. Since linux 4.8, the sysfs interface has been depricated and it is recommended to use charcter devices instead. This demo will walk through some basic demos to show functionality interacting with the GPIO.

## Basic Installation Steps <br/>
The old version of gpiod(v1.5.4) was depricated and the below sample code has been based on the current release. You will need at least v2.0.2. Depending on your installed version of Jetpack, you likely have a depricated version of libgpiod installed for system functions. We want to make sure the user calls upon a recent version:
- Open a terminal session
- First we should ensure are system is up to date ``` sudo apt-get upgrade ```
- libgpiod depends on ``` python3-dev``` , this should already been installed, but just in case we can run ```sudo apt install python3-dev```
- Next we can install gpiod. ```pip install gpiod```.
  - Ensure this installs a version later than 2.0.2.
  - If you see 1.5.4 being installed, you can run ```pip uninstall gpiod``` and then ```pip install gpiod==2.0.2``` .
  - If you encounter an error that a version of the package is not available, You should upgrade your Jetson to a newer version of Jetpack before continuing. Reference our [Jetpack 6 upgrade guide](https://github.com/onlogic/Updating-to-Jetpack-6-for-Aetina-Jetson.git) for more information.

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

We will use NX GPIO 1 for the following examples. We can call upon these pins to set an output (High/Active = 3.3V) (Low/Inactive = 0V) or set as an input. For a full list of features vist the python binding examples as part of the lipgpiod library.

## Libgpiod Command Line
Even though we have the line numbers above. You can easily identify relevant lines with the included CLI. To interface with GPIO pins we need to know the chip it is on and then the line (We can use either the GPIO Name (ex. PQ.05) or the chip line (105) in most cases). <br/>
``` gpioinfo``` will allow us to list all of the chips and their lines. Let's find the info we need for GPIO01. Here we can see that gpiochip0 contains our address. <br/>
![gpioinfo cli](/assets/gpioinfo1.png) <br/>
Scrolling down to PQ.05 shows us that gpiochip0 shows us that are line is 105. <br/>
![gpioinfo cli](/assets/gpioinfo2.png) <br/>

There are additional cli commmands avaiable such as ```gpioget``` and ```gpioset``` for temporarily reading and setting values. ```gpiomon``` which waits for edge events and ```gpionofity``` which waits for state changes. More info on usage can be found on the libgpiod readme.

## Libgpiod Sample Code







