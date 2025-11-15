# TinyPLC

NOTE: This project is under construction. Do not expect everything to work just yet.

## What is it?
This project provides a small and easy-to-use open-source PLC (programmable logic controller) hardware / software platform intended for small automation and control tasks, built around a Raspberry Pi Pico 2W.

## Who is it for?
TinyPLC aims towards hobbyist developers and electrical engineers who want to easily automate stuff in the physical world with Python, but have been limited due to the lack of peripheral hardware connected to their microcontrollers, until now!

### Hardware features:
- 5V supply voltage
- 4 isolated digital inputs (5V to 24V, isolated external 5V supply through DC/DC converter)
- 4 relay outputs (contact: NO, up to 230V, 10A)
- SPI interface
- I²C interface
- 6 GPIOs (3,3V)
- custom 3D printable enclosure

### Software features:
- controller programmed in MicroPython
- slim PLC framework with user-defined initialization and loop function
- open-source
- possibility to use the WiFi/Bluetooth capabilities of the used Rasperry Pi Pico 2W board to build your own wireless controller

## License and Disclaimer
This project is released under the MIT license. Feel free to use it for your projects, as long as you know what you are doing when dealing with electrics/electronics. I am not liable to any harm you are causing to yourself, others or someone's property when using the provided files. Do not use TinyPLC with dangerous voltages or for safety-critical applications and follow the regulations and laws applicable in your location!
