# I<sup>2</sup>C

[I<sup>2</sup>C](https://en.wikipedia.org/wiki/I2C) is an acronym for ***Inter Integrated Circuit*** , which is used for attaching lower-speed peripheral ICs to processors and microcontrollers in short-distance, intra-board communication.

In this section, we will describe the I<sup>2</sup>C protocol.

## What is I<sup>2</sup>C?

I<sup>2</sup>C is a *serial protocol* to connect *low-speed* devices like microcontrollers, EEPROMs, A/D and D/A converters, I/O interfaces and other similar peripherals in embedded systems.

I<sup>2</sup>C is a *multi-master, multi-slave, synchronous, bidirectional, half-duplex* serial communication bus.

I<sup>2</sup>C-bus is used in various control architectures such as System Management Bus (SMBus), Power Management Bus (PMBus), Intelligent Platform Management Interface (IPMI), Display Data Channel (DDC) and Advanced Telecom Computing Architecture (ATCA).

## I<sup>2</sup>C bus

The I<sup>2</sup>C bus uses two wires: serial data (SDA) and serial clock (SCL). All I<sup>2</sup>C master and slave devices are connected with only those two wires.

<p align="center">
    <img src="https://files.catbox.moe/npfpvh.png"><br>
    Typical I<sup>2</sup>C Connection Diagram
</p>

Each device can be a transmitter, a receiver or both. Some devices are masters – they generate bus clock and initiate communication on the bus, other devices are slaves and respond to the commands on the bus.

In order to communicate with specific device, each slave device must have an address which is unique on the bus. I<sup>2</sup>C master devices (usually microcontrollers) don’t need an address since no other (slave) device sends commands to the master.

### Bus signals

Both signals (SCL and SDA) are bidirectional. They are connected via resistors to a positive power supply voltage. This means that when the bus is free, both lines are high. All devices on the bus must have open-collector or open-drain pins. Activating the line means pulling it down.

The number of the devices on a single bus is almost unlimited – the only requirement is that the bus capacitance does not exceed 400 pF. Because logical 1 level depends on the supply voltage, there is no standard bus voltage.

### Serial data transfer

For each clock pulse one bit of data is transferred. The SDA signal can only change when the SCL signal is low – when the clock is high the data should be stable.

<p align="center">
    <img src="https://files.catbox.moe/wu2fjm.gif">
</p>

### Start and Stop condition

Each I<sup>2</sup>C command initiated by master device starts with a **START condition** and ends with a **STOP condition**. For both conditions SCL has to be high. A high to low transition of SDA is considered as START and a low to high transition as STOP.

<p align="center">
    <img src="https://files.catbox.moe/x7889v.gif">
</p>

After the Start condition the bus is considered as busy and can be used by another master only after a Stop condition is detected. After the Start condition the master can generate a repeated Start. This is equivalent to a normal Start and is usually followed by the slave I<sup>2</sup>C address.

Microcontrollers that have dedicated I<sup>2</sup>C hardware can easily detect bus changes and behave also as I<sup>2</sup>C slave devices. However, if the I<sup>2</sup>C communication is implemented in software, the bus signals must be sampled at least two times per clock cycle in order to detect necessary changes.

### I<sup>2</sup>C data transfer

Data on the I<sup>2</sup>C bus is transferred in 8-bit packets (bytes). There is no limitation on the number of bytes, however, each byte must be followed by an Acknowledge bit. This bit signals whether the device is ready to proceed with the next byte. For all data bits including the Acknowledge bit, the master must generate clock pulses.

<p align="center">
    <img src="https://files.catbox.moe/v038sk.gif">
</p>

If the receiver device does not acknowledges transfer this means that there is no more data or the device is not ready for the transfer yet. The master device must either generate Stop or Repeated Start condition.

<p align="center">
    <img src="https://files.catbox.moe/zyaptd.gif">
</p>

#### Synchronization

Each master must generate its own clock signal and the data can change only when the clock is low. For successful bus arbitration a synchronized clock is needed. Once a master pulls the clock low it stays low until all masters put the clock into high state. Similarly, the clock is in the high state until the first master pulls it low. This way by observing the SCL signal, master devices can synchronize their clocks.

#### Arbitration

For normal data transfer on the I<sup>2</sup>C bus only one master can be active. If for some reason two masters initiate I<sup>2</sup>C command at the same time, the arbitration procedure determines which master wins and can continue with the command.

Arbitration is performed on the SDA signal while the SCL signal is high. Each master checks if the SDA signal on the bus corresponds to the generated SDA signal. If the SDA signal on the bus is low but it should be high, then this master has lost arbitration. Master I<sup>2</sup>C device that has lost arbitration can generate SCL pulses until the byte ends and must then release the bus and go into slave mode. The arbitration procedure can continue until all the data is transferred. This means that in multi-master system each I<sup>2</sup>C master must monitor the I<sup>2</sup>C bus for collisions and act accordingly.

#### Clock synchronization and Handshaking

Slave devices that need some time to process received byte or are not ready yet to send the next byte, can pull the clock low to signal to the master that it should wait. Once the clock is released the master can proceed with the next byte.

#### Communication with 7-bit I<sup>2</sup>C addresses

<p align="center">
    <img src="https://files.catbox.moe/bczxpm.gif">
</p>

Each slave device on the bus should have a unique 7-bit address. The communication starts with the Start condition, followed by the 7-bit slave address and the data direction bit. If this bit is 0 then the master will write to the slave device. Otherwise, if the data direction bit is 1, the master will read from slave device. After the slave address and the data direction is sent, the master can continue with reading or writing.

The communication is ended with the Stop condition which also signals that the I<sup>2</sup>C bus is free. If the master needs to communicate with other slaves it can generate a repeated start with another slave address without generation Stop condition. All the bytes are transferred with the MSB bit shifted first.

<p align="center">
    <img src="https://files.catbox.moe/nmis2v.gif"><br>
    The master only writes to the slave device
</p>

<p align="center">
    <img src="https://files.catbox.moe/nmis2v.gif"><br>
    The master only reads to the slave device
</p>

Sometimes the master needs to write some data and then read from the slave device. In such cases it must first write to the slave device, change the data transfer direction and then read the device. This means sending the I<sup>2</sup>C address with the R/W bit set to write and then sending some additional data like register address. After writing is finished the master device generates repeated start condition and sends the I<sup>2</sup>C address with the R/W bit set to read. After this the data transfer direction is changed and the master device starts reading the data.

<p align="center">
    <img src="https://files.catbox.moe/aclnm7.gif"><br>
    The master reads and writes to the slave device<
</p>

## Extension of the I<sup>2</sup>C specifications

Standard mode of I<sup>2</sup>C bus uses transfer rates up to 100 kbit/s and 7-bit addressing. With the advance of the technology, needs for higher transfer rates and larger address space emerged.

### Bus speeds

- Fast Mode – supports transfer rates up to 400 kbit/s.
- High-speed mode (Hs-mode) – supports transfer rates up to 3.4 Mbit/s.

There can by any combination of the devices on the bus regardless of the supported speed and addressing. Fast mode devices are downward-compatible and can work with slower I<sup>2</sup>C controllers. However, most modern I<sup>2</sup>C controllers support all speeds and addressing modes.

High-speed mode uses signals called SCLH and SDAH to emphasize the higher speed. These signals are usually separated from standard SDA and SCL lines. High-speed mode introduces also few differences (or improvements) in the specifications:

- Improved data and clock line output drivers.
- Schmitt trigger and spike suppression circuits on data and clock inputs.
- Clock synchronization and arbitration is not used.
- Clock signal has 1 to 2 high/low ratio.

### 10-bit I<sup>2</sup>C Addressing

In some cases it is very hard to avoid address collisions since 7 bits for I<sup>2</sup>C addresses allow only 127 different addresses where only 112 can actually be used. Some I<sup>2</sup>C devices on the board, despite address pins, have the same address.

10-bit addressing can be used together with 7-bit addressing since a special 7-bit address (1111 0XX) is used to signal 10-bit I<sup>2</sup>C address. When a master wants to address a slave device using 10-bit addressing, it generates a start condition, then it sends 5 bits signaling 10-bit addressing (1111 0), followed by the first two bits of the I<sup>2</sup>C address and then the standard read/write bit.

<p align="center">
    <img src="https://files.catbox.moe/lkav2z.gif">
</p>

If the master will write data to the slave device it must send the remaining 8 bits of slave address as the second byte.

If the master will read data from the slave device it must send the complete 10-bit address (two bytes) as for writing, then a repeated start is sent followed by the first address byte with read/write bit set to high to signal reading. After this procedure the data can be read from the slave device.

<p align="center">
    <img src="https://files.catbox.moe/ojr6se.gif">
</p>
