#!/usr/bin/env python3

#Original Sample Code by 2023 Kent Gibson <warthog618@gmail.com>, GPL-2.0-or-later License
#Modified by OnLogic for demonstration purposes

"""Minimal example of reading the info for a line."""

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
