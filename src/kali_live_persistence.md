# A easy way to build your own kali live System

## #0x01 Download kali live image
Download kali live iamge from [Download url](https://www.kali.org/downloads/). 

**Note** make sure you have checked SHA256.
## #0x02 Write kali live into USB
The easiest way to write a kali live image is using [rufus](https://rufus.ie/) to write into your thumb drive.

**Note** leave enough space for boot.
E.g. you have a 32GB USB and download a 3GB kali live image, then you should leave 3-4GB for boot and anthor part for your kali live persistence.

## #0x03 Install nvidia dirver
If you want nvidia graphics card enabled, make sure #nouveau# is **down** when you install nvidia driver.
**Note** select kali persistence to enter.

Once you have that ready boot to your kali persistence.

    apt-get update && apt-get upgrade -y && apt-get dist-upgrade –y
    apt-get install linux-headers-$(uname -r) –y
    reboot


