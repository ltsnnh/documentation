# Functional Description

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
- **MISO**: Master In / Slave Out data
- **MOSI**: Master Out / Slave In data
- **SCK**: Serial Clock output for SPI masters and input for SPI slaves
- **NSS**: Slave select

### General

#### Slave select (NSS) pin management

- **Software NSS management**: The slave select information is driven internally, the external NSS pin remains free
- **Hardware NSS management**
    - **NSS output enabled**: only master mode
    - **NSS output disabled**: multimaster capability for devices operating in master mode and classic slave mode

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

#### Procedure

1. Define 8- or 16-bit data frame format
2. Select the CPOL and CPHA
3. The frame format MSB-first or LSB-first
4. Configure NSS pin
5. Select Slave Mode and enable SPI

#### Transmit sequence

The data byte is parallel-loaded into the Tx Buffer during a write cycle.

The transmit sequence begins when the slave device receives the clock signal and the most significant bit of the data on its MOSI pin.  
The remaining bits are loaded into the shift-register.  
The TXE flag is set on the transfer of data from the Tx Buffer to the shift register and an interrupt is generated if the TXEIE bit is set.

#### Receive sequence

The data in shift-register is transferred to Rx Buffer.

The RXNE flag is set.  
An interrupt is generated if the RXNEIE bit is set.  
Clearing of the RXNE bit is performed by reading the SPI_DR register.

### Configuring the SPI in master mode

#### Procedure

1. Define the serial clock baud rate
2. Select the CPOL and CPHA
3. Define 8- or 16-bit data frame format
4. Configure the LSBFIRST bit
5. Configure NSS pin
6. Select Master Mode and enable SPI

#### Transmit sequence

The transmit sequence begins when a byte is written in the Tx Buffer.

The data byte is parallel-loaded into the shift-register during the first bit transmission and then shifted out serially to the MOSI pin.
The TXE flag is set on the transfer of data from the Tx Buffer to the shift register.
An interrupt is generated if the TXEIE bit is set.

#### Receive sequence

The data in shift-register is transferred to Rx Buffer.

The RXNE flag is set.  
An interrupt is generated if the RXNEIE bit is set.  
Clearing of the RXNE bit is performed by reading the SPI_DR register.

[NOTE: If SPI slaves which need to be de-selected between transmissions, the NSS pin must be configured as GPIO which toggled by software.]

### Configuring the SPI for half-duplex communication

The SPI is capable of operating in half-duplex mode in 2 configurations.
- 1 clock and 1 bidirectional data wire
- 1 clock and 1 data wire (receive-only or transmit-only)

### Data transmission and reception procedures

#### Handling data transmission and reception

1. Enable the SPI by setting the SPE bit to 1
2. Write the first data item to be transmitted into the SPI_DR register (this clears the TXE flag)
3. Wait until TXE=1 and write the second data item to be transmitted. Then wait until RXNE=1 and read the SPI_DR to get the first received data item (this clears the RXNE bit). Repeat this operation for each data item to be transmitted/received until the n–1 received data
4. Wait until RXNE=1 and read the last received data
5. Wait until TXE=1 and then wait until BSY=0 before disabling the SPI

This procedure can also be implemented using dedicated interrupt subroutines launched at each rising edges of the RXNE or TXE flag.

### CRC calculation

### Status flags

#### Tx buffer empty flag (TXE)

#### Rx buffer not empty (RXNE)

#### BUSY flag (BSY)

This BSY flag is set and cleared by hardware . The BSY flag indicates the state of the communication layer of the SPI. When BSY is set, it indicates that the SPI is busy communicating.

### Disabling the SPI

When a transfer is terminated, the application can stop the communication by disabling the SPI peripheral.

### SPI communication using DMA (direct memory addressing)

### Error flags

#### Master mode fault (MODF)

#### Overrun condition

When the master device has sent data bytes and the slave device has not cleared the RXNE bit resulting from the previous data byte transmitted.

The newly received data is lost.

#### CRC error

### SPI interrupts

| Interrupt event | Event flag | Enable Control bit |
| :---: | :---: | :---: |
| Transmit buffer empty flag | TXE | TXEIE0 |
| Receive buffer not empty flag | RXNE | 1RXNEIE |
| Master Mode fault event | MODF | ERRIE |
| Overrun error | OVR | ERRIE |
| CRC error flag | CRCERR | ERRIE |
