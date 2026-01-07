SPI
================================================================================

The serial peripheral interface (SPI) allows half/ full-duplex, synchronous, serial communication with external devices. By default, it is the SPI function that is selected. It is possible to switch the interface from SPI to I<sup>2</sup>S by software. The I<sup>2</sup>S audio protocol is only supported in high-density, XL-density and connectivity line devices.

SPI features:

- Full-duplex synchronous transfers on three lines
- Simplex synchronous transfers on two lines with or without a bidirectional data line
- 8- or 16-bit transfer frame format selection
- Master or slave operation
- Multimaster mode capability
- 8 master mode baud rate prescalers (f<sub>PCLK</sub>/2 max)
- Slave mode frequency (f<sub>PCLK</sub>/2 max)
- Faster communication for both master and slave
- NSS management by hardware or software for both master and slave: dynamic change of master/slave operations
- Programmable clock polarity and phase
- Programmable data order with MSB-first or LSB-first shifting
- Dedicated transmission and reception flags with interrupt capability
- SPI bus busy status flag
- Hardware CRC feature for reliable communication:
    - CRC value can be transmitted as last byte in Tx mode
    - Automatic CRC error checking for last received byte
- Master mode fault, overrun and CRC error flags with interrupt capability
- 1-byte transmission and reception buffer with DMA capability: Tx and Rx requests

--------------------------------------------------------------------------------

.. toctree::
	:maxdepth: 2

	spi
