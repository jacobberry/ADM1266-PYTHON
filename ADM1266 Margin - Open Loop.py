# Copyright (c) 2017 Analog Devices Inc.
# All rights reserved.
# www.analog.com

#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#==========================================================================


# Release Notes -----------------------------------------------------------
# This script uses the Aardvark from Total Phase drivers to communicate with ADM1266.
# If you would like to use other devices, please comment out the Aardvark sections below.
# Open PMBus_I2C.py and replace aardvark_py APIs with the dongle APIs that you are using.
# No other modification is required

import PMBus_I2C
import ADM1266_Lib
import sys

if sys.version_info.major < 3:
    input = raw_input

if __name__ == '__main__':

    # Open Connection to Aardvark (Comment this section out for using other devices other than Aardvark)
    # If no dongle ID is passed into the function an auto scan will be performed and the first dongle found will be used
    # For using a specific dongle pass the unique ID number, as shown in example below.
    # Example: PMBus_I2C.Open_Aardvark(1845957180)
    PMBus_I2C.Open_Aardvark()

    # PMBus address of all ADM1266 in this design. e.g: [0x40, 0x42]
    ADM1266_Lib.ADM1266_Address = [0x40, 0x42]

    # Check if all the devices listed in ADM1266_Lib.ADM1266_Address above is present. 
    # If all the devices are not present the function will throw an exception and will not procced with the remaining code.
    ADM1266_Lib.device_present()

    # Check if memory refresh is running
    if ADM1266_Lib.refresh_status() == True:
        print("Memory refresh is currently running, please try after 10 seconds.")

    else:
        # ADM1266_Lib.margin_single(Device address, Physical pin Name to be margined)
        # Take user input for device address
        address = input("Enter device address (e.g. 0x40): ")        
        # Take user input for DAC name
        dac = input("Enter DAC name (e.g. DAC1, DAC2): ")
        # # Take user input for DAC output voltage
        dac_output = input("Enter DAC output voltage in between 0.202V - 1.565V (e.g. 1.223): ")
        
        # dac_config function checks if the DAC is configured an open loop, if not it will ask the user. 
        # User can decide to configure the closed loop or disable DAC to open loop, or skip open loop margining.        
        if ADM1266_Lib.dac_config(address, dac):            
            # If the DAC is configured as open loop margin_open_loop sets the DAC output to the requested voltage.
            ADM1266_Lib.margin_open_loop(address, dac, dac_output) 

    # Close Connection to Aardvark ( Comment this section out for using other devices other than Aardvark)
    PMBus_I2C.Close_Aardvark()