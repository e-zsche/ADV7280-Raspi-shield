# Even more control over picture quality

While doing picture adjustment via v4l2-ctl is fine it's not the end of it! You can have even
more control when starting to set values in the ADV7280 registers.

There is only one problem: the kernel has ownership of the I2C interface so you should not be
able to read and write directly on the bus. Well, kind of... There is a really hacky und unsafe
way to get around this. What you need is a small utility package for interfacing with i2c over
the command line.

```
sudo apt install i2c-tools
```

Inside the package are two tools that let us get access to blocked I2C busses: `i2cget` and `i2cset`.
All of this is packed in a messy python library that basically calls the command line tools and
reads the output.

As you can imagine this whole process is really messy as you never check if there is other traffic
on the bus at any time. From what I can tell the ADV7280 gets initialized by the kernel module
at boot time and afterwards it just occupies the bus with no more commands being issued. Until now
there were no crashes because of colliding I2C commands.

You can however make the chip unresponsive by setting some values in the registers. Be warned. Should
this happen and there is no response from the chip you can just reboot and everything works fine again.

## ADV7280 registers

If you want to see the registers and what they do for yourself Analog Devices published the <a href="https://www.analog.com/media/en/technical-documentation/user-guides/adv7280_7281_7282_7283_ug-637.pdf">hardware reference pdf</a>
for the ADV7280 (and similiar). Here you will find all registers with description and what they do
