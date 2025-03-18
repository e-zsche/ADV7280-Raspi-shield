# ADV7280 based analog video digitizer shield for raspberry pi

Raspberry pi shiel built around the ADV7280 analog video decoder IC. Connection to raspberry pi over
MIPI CSI-2 interface. FFC/FPC connector on the shield has the same pinout as the pi camera connector.

<img src"pic/raspi_with_adv_shield.jpg" alt="isolated" width="450" />

One huge advantage the ADV7280 has over similiar analog video decoders is that the drivers are already
present in the standard raspberry pi linux kernel. All you have to do is enable the driver in the
config.txt file. This shield is more or less plug'n'play.
