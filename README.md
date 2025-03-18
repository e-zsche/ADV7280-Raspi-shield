# ADV7280 based analog video digitizer shield for raspberry pi

Raspberry pi shiel built around the ADV7280 analog video decoder IC. Connection to raspberry pi over
MIPI CSI-2 interface. FFC/FPC connector on the shield has the same pinout as the pi camera connector.

<p float="center">
  <img src="pic/raspi_with_adv_shield.jpg" width="600" />
</p>

One huge advantage the ADV7280 has over similiar analog video decoders is that the drivers are already
present in the standard raspberry pi linux kernel. All you have to do is enable the driver in the
config.txt file. This shield is more or less plug'n'play.

# Hardware

The whole circuit design is copied exactly from the ![ADV7280 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ADV7280.PDF)

Video inputs are done with BNC connectors. The only reason is that I got these really cheap so I use
them everywhere. All video inputs are terminated with 75R resistors close to the connector. For
protection there are BAT54S diodes installed on all used inputs. Because of space constraints only
inputs 1 - 4 are available on the PCB.

In the beginning I was unsure how to set the RST, PWRDWN pins of the ADV7280 and how important
the power cycling is when booting the IC. That is what the jumper pins near the raspberry pi's
USB connectors are for. Turns out you can leave them all connected to +3.3V all the time.

I was unsure about the CAM_IO1 and CAM_IO2 pins of the raspberry CSI connector as well. The pins
on the pin header can be left unconnected.

The only really critical traces in my opinion are from the CSI output from the IC to the FFC/FPC
camera connector. Looking at the technical specs in the MIPI CSI standard these traces the traces
should have 100R differential impedance (+/- 10%). To get the correct trace width and spacing I
used kicad's builtin calculation tool and the PCB dimensions of the manufacturer. With these I
fiddled around with the calculation until it was close enough.

This design is routed for ordering at JLCPCB (not sponsored!). This is important because different
manufacturers may have different PCB dimensions, which in turn affects the trace impedance of the
CSI traces. Make sure to get this correct, otherwise the CSI connection may not work reliably.

Until now the shield is running fine and I encountered no problems while running.
