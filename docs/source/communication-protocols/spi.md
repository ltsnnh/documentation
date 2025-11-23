# SPI (Serial Peripheral Interface)

SPI is an acronym for ***Serial Peripheral Interface***, which is used to communicate between microcontrollers and peripheral devices (like Flash Memories, ADC, DAC, RTC, LCD, SDcards, and much more).

In this section, we will describe the SPI protocol.

## What is SPI?

SPI is a communication protocol typically used for *serial communication* between microcomputer systems and other devices, memories, and sensors. Put simply, it’s a system that allows us to *send a byte* to some device and *receive a byte* in return.

SPI uses what’s called *a Master-Slave architecture*. There is one master device that communicates to multiple slave devices. In most cases, the master device is microcontroller and the slave devices are sensors. The master can only communicate with one slave device at a time and the slaves cannot communicate with each other.

## SPI bus

In digital systems, data is transferred in the form of 1’s and 0’s. In hardware, 1’s and 0’s are represented as high and low voltages. Many systems use 3.3V, so a 1 corresponds to ~3.3V on the wire and a 0 corresponds to ~0V, while others use 5V to correspond to a 1.

SPI is a *synchronous* communication protocol, meaning data is timed with clock pulses. Data is sent and received at the same time, turn SPI a *full-duplex* communication. This means that two of the four lines (MOSI, MISO) are for data, and one of the lines (SCK) is for timing.

SPI uses four wires to communicate, which are referred to as the SPI bus. Line SCK is shared between all devices on a SPI bus. Lines (MOSI, MISO, CS/SS) are connected depends on SPI bus configurations.

The master device always transmits a square wave on SCK (source clock) to synchronize all devices. To initiate communication (in independent slave mode - normal mode), the master device sets CS/SS (chip select/slave select) low for a particular device. The master device sends data to the slave device on the MOSI (master out, slave in) line. At the same time, the slave device sends data to the master device on the MISO (master in, slave out) line. To stop communication, the master devices sets CS/SS high again.

<p align="center">
    <img src="https://files.catbox.moe/0jyafc.jpg" width="512">
</p>
<p align="center">Typical SPI Connection Diagram</p>

### SCK/SCLK (Source Clock)

The clock keeps the data lines and devices in sync. The clock is an oscillating signal produced by the master device that tells the receiving device when to read the data. Depending on the device properties, data is either sent/received on the rising/falling edge of SCK. This line is shared by all slave devices.

### MOSI (Master Out Slave In)

This is the line where data is sent from the master device to the slave device.

### MISO (Master In Slave Out)

On this line the data is being sent out of the slave device received by master.

### CS/SS (Chip Select / Slave Select)

This line is referred to as CS or SS interchangeably. It is active low, which means the slave device is active when CS is set low. Only one CS can be low at a time or there will be conflicts on the SPI bus resulting in garbage data.

There is usually a pull-up resistor on the CS pin to set a default value. A pull-up resistor is a large resistor (typically 10K) which bridges between VCC and another pin. When no load is applied to the pin, no current flows through the resistor. This allows us to hold CS at a known (VCC) state when the CS pin isn’t being driven by other circuitry. Then, we can drive another pin on the CS line low (GND) to select the device. Current will flow through the resistor and drop VCC across it.

### Hardware signal

<p align="center">
    <img src="https://files.catbox.moe/a5owi4.png" width="512">
</p>
<p align="center">SPI signals on an oscilloscope</p>

You can’t really distinguish between MISO and MOSI in this picture but just pick one to be MOSI and the other to be MISO.

*Which lines are which?*
- The **yellow line is CS**. It is being lowered before and raised after the SPI transfer is complete.
- The **green line is SCK**. It oscillates 8 times for each byte sent.
- The **pink and blue are MOSI and MISO**. The blue line has `0x00` and `0x00` and the pink line has `0b10010101` and `0b01010101`

## SPI configuration

### Modes of operation

Devices on the SPI bus can operate in either mode of the following: **Master** or **Slave**. There must be at least one master which initiates the serial communication process. On the other hand, there can be single or multiple devices operating in slave mode.

The master device can select which slave to talk to by setting the **SS** (slave select) pin to logic low. If a single slave is being addressed, you can tie the SS pin of this slave device to logic low without the need to control this line by the master.

### Clock rate

The Master device on the SPI bus has to configure and generate the clock signal at the beginning of any communication. During each SPI clock cycle, full-duplex data transmission occurs. The master sends a bit on the MOSI line and the slave reads it, while the slave sends a bit on the MISO line and the master reads it.

This sequence is maintained even when only one-directional data transfer is intended. Which means in order to receive any data you have to actually send something! in this case, we call it “Dummy Data” or “Junk”!

Theoretically, the clock rate can be whatever you want provided that it’s practically realizable. The SPI serial clock is derived from the CLKsys of your system, which means it can by Fosc/2 or 4, 8, 16 or whatever. The dynamic range starts from a few KHz up to several MHz. (Practical limitations are case-dependent for each system).

### Clock Polarity, Clock Phase

The SPI Master device should also configure the clock polarity (CKP) and clock phase (CKE). The clock polarity & phase together determine when will the data be latched on the data line.

**CKP** can be configured to be 1 or 0. Which means you can set the default state of the clock (the IDLE) to be high or low whichever you want.
- For (CKP = 0), the clock IDLEs at 0, and each cycle consists of a pulse of 1. That is, the leading edge is a rising edge, and the trailing edge is a falling edge.
- For (CKP = 1), the clock IDLEs at 1, and each cycle consists of a pulse of 0. That is, the leading edge is a falling edge, and the trailing edge is a rising edge.

**CKE** can be configured to be 1 or 0. Which means you can set the edge on which the data will be latched whether it’s a rising or falling edge (leading or trailing).
- For (CKE = 0), the “out” side changes the data on the trailing edge of the preceding clock cycle, while the “in” side captures the data on (or shortly after) the leading edge of the clock cycle.
- For (CKE = 1), the “out” side changes the data on the leading edge of the current clock cycle, while the “in” side captures the data on (or shortly after) the trailing edge of the clock cycle.

<p align="center">
    <img src="https://files.catbox.moe/9wr2m5.jpg" width="512">
</p>
<p align="center">SPI Clock Phase And Polarity Table</p>

You have to refer to the device’s datasheet in order to set both CKP & CKE properly. If the SPI Master doesn’t configure the CKP (clock polarity) & CKE (clock phase) to what the slave device expects, any sort of communication (write/read) will fail.

### Mode numbers 

The combination of both clock polarity and phase is commonly referred to as “SPI Mode”.

| SPI Mode | CPOL | CPHA |
| :---: | :---: | :---: |
| 0 [00] | 0 | 0 |
| 1 [01]| 0 | 1 |
| 2 [10] | 1 | 0 |
| 3 [11] | 1 | 1 |

## SPI bus configurations

All devices on the SPI bus including the master and all slaves can all be connected in a couple of different configurations. Which mostly depend on how they are manufactured and how data should be flowing through the network of devices in that particular application. I’ll briefly describe both of these configurations hereafter.

### Daisy chain

Each device is connected between 2 other devices in a circular (logically) way as shown in the diagram down below. [NOTE: a logical circle is a term that describes data circulation flow in the network which means that devices connection doesn’t necessarily need to be circular in shape]

<p align="center">
    <img src="https://files.catbox.moe/1zm14k.jpg" width="512">
</p>
<p align="center">SPI Daisy Chain Configuration</p>

The SPI port of each slave device is designed to send data out during the second group of clock pulses an exact copy of the data it received during the first group of clock pulses. The whole chain acts as a communication shift register. Each slave copies the input data to the output in the next clock cycle until the SS line goes high. Such a feature only requires a single SS line from the master, rather than a separate SS line for each slave.

That means a data frame will keep propagating through slave devices as long as the SS line is held low.

<p align="center">
    <img src="https://files.catbox.moe/ikeova.png" width="512">
</p>
<p align="center">Single SPI master addresses multiple slave devices using only one SS line</p>

### Independent slave

In the independent slave configuration, there is an independent slave select line for each slave. This is the way SPI is normally used. The master asserts only one chip select at a time.

<p align="center">
    <img src="https://files.catbox.moe/3v7i78.png" width="512">
</p>
<p align="center">SPI Independent Slave Configuration</p>

As you can see, this configuration can be impractical in case your system involves many SPI slave devices. Which will require too many IO pins to control all SS lines.

## Why SPI is needed (or not)?

### Advantages

- Full-Duplex serial communication.
- Potentially high-speed data transfer rates.
- Few wires are required for the bus (typically 4 lines).
- Extremely flexible data transfer. It’s not limited to 8-Bits, it can be any arbitrarily-sized words.
- Slaves don’t need unique addresses (unlike I2C).
- Slaves use the master’s clock and do not need precision oscillators (unlike UART).
- Transceivers are not needed (unlike CAN).

### Disadvantages

- No hardware slave acknowledgment (the master could be transmitting to nowhere without knowing).
- Typically supports only one master device.
- Requires more pins (unlike I2C).
- No hardware-level error-checking protocol is defined.
- Can only support very short distances (usually onboard communications) compared to RS-232 and CAN-Bus.
