Communication Protocols
================================================================================

There are various communication protocols used in the embedded system to communicate data between devices. Different protocols have different hardware (communication lines) and transfer data in different formats. Different protocols prioritize different things, such as error checking, minimal hardware wires, or message priorities.

- CAN - generally be used to communicate between the microcontrollers in different subsystems.
- SPI - generally be used by each microcontroller to communicate with flash memories, sensors and other devices within its subsystem.
- UART - generally be used to communicate between a microcontroller and a laptop. It can send log messages to the laptop (useful for debugging) or receive keyboard input from the laptop (not used much, but sometimes for controlled testing).

--------------------------------------------------------------------------------

.. toctree::
	:maxdepth: 2

	spi
	i2c
