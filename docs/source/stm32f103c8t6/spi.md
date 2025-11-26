# SPI

The serial peripheral interface (SPI) allows half/ full-duplex, synchronous, serial communication with external devices. By default, it is the SPI function that is selected. It is possible to switch the interface from SPI to I<sup>2</sup>S by software. The I<sup>2</sup>S audio protocol is only supported in high-density, XL-density and connectivity line devices.

## SPI features

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

## SPI functional description

<p align="center">
    <img src="https://files.catbox.moe/icea8y.png" width="512"><br>
    Single master/ single slave application
</p>

Usually, the SPI is connected to external devices through four pins:
- **MISO**: Master In / Slave Out data. 
- **MOSI**: Master Out / Slave In data.
- **SCK**: Serial Clock output for SPI masters and input for SPI slaves.
- **NSS**: Slave select.

### General

#### Slave select (NSS) pin management

- **Software NSS management**: The slave select information is driven internally, the external NSS pin remains free.
- **Hardware NSS management**
    - **NSS output enabled**: only master mode.
    - **NSS output disabled**: multimaster capability for devices operating in master mode and classic slave mode.

#### Clock phase and clock polarity

The combination of the **CPOL** (clock polarity) and **CPHA** (clock phase) bits selects the data capture clock edge.

Master and slave must be programmed with the same timing mode.

<p align="center">
    <img src="https://files.catbox.moe/69ld11.png" width="512"><br>
    Data clock timing diagram
</p>

#### Data frame format

Data can be shifted out either **MSB-first or LSB-first** and each data frame can be **8 or 16 bits** long.

### Configuring the SPI in slave mode

#### Transmit sequence

The data byte is parallel-loaded into the Tx Buffer during a write cycle.

The transmit sequence begins when the slave device receives the clock signal and the most significant bit of the data on its MOSI pin.  
The remaining bits are loaded into the shift-register.  
The TXE flag is set on the transfer of data from the Tx Buffer to the shift register and an interrupt is generated if the TXEIE bit is set.

#### Receive sequence

The data in shift register is transferred to Rx Buffer.

The RXNE flag is set.  
An interrupt is generated if the RXNEIE bit is set.  
Clearing of the RXNE bit is performed by reading the SPI_DR register.

### Configuring the SPI in master mode
