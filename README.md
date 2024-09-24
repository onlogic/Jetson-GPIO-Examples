#Utilizing GPIO for production Jetson systems

This guide will walk you through utilizing GPIO pins on the 15-pin header located on the rear of your Jetson device with the [libgpiod C library](https://github.com/brgl/libgpiod), specifically the command line interface and simple Python sample code to demonstrate key concepts.
> [!WARNING]
> Any Python Code in this repository is purely for demonstration and testing purposes, it is not production ready. Please ensure to visit libgpiod repository for more info on [python-based bindings](https://github.com/brgl/libgpiod/tree/master/bindings/python).

## Jetson GPIO Pin Basics <br/>

Let's first take a brief look at the GPIO pins available. Each Jetson system has a DB15 connector located on the rear of the system. The top 5 pins are our GPIO pins. For this guide, we will use a NX system as the PIN addresses are listed in the [system manual](https://www.dropbox.com/scl/fi/o4rogjf4r6nldqs6ow7e8/Aetina_AIE-PO22_32_PN32_42_user-manual.pdf?rlkey=d85bauvq4isimlzmu8hwtrq8r&e=1&dl=0). For simplificity you can find that in the below table.

| GPIO Physical Pin # | Linux Pin Name|
| --- | --- |
| GPIO 1 | PQ.05 |
| GPIO 2 | PQ.06 |
| GPIO 3 | PN.01|
| GPIO 4 | PH.00 |
| GPIO 5 | PZ.07 |

All python examples will use pin 1 for consistentcy.

##Getting Started with command line
TO-DO: Test on older system to see what happens without anything installed for both CLI and python code
