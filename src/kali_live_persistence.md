---
layout: post
title: A easy way to build your own kali live system
slug: kali_live_persistence
date: 2020-09-19 19:54
status: publish
author: CrazyDogen
categories: 
  - Kali
tags: 
  - Kali live persistence
excerpt: a easy way to install kali live persistence
---

Using a kali live persistence is kind of compromise of choosing daily OS.
However, I notice that it's a troublesome experience to install a kali live persistence. Here is my easy way to install it.
## #0x01 Download kali live image
Download kali live image from [Offical download url](https://www.kali.org/downloads/). 

**Note** make sure you have checked SHA256.
## #0x02 Write kali live into USB
The easiest way to write a kali live image is using [rufus](https://rufus.ie/) to write into your thumb drive.

**Note** leave enough space for boot.
E.g. you have a 32GB USB and download a 3GB kali live image, then you should leave 3-4GB for boot and anthor part for your kali live persistence.

If you want encrypted persistence, refer to [Adding Persistence to a Kali Linux "Live" USB Drive](https://www.kali.org/docs/usb/kali-linux-live-usb-persistence/#:~:text=The%20persistent%20data%20is%20stored,article%20will%20show%20you%20how.).

## #0x03 Install nvidia dirver and cuda
If you want nvidia graphics card enabled, make sure #nouveau# is **down** when you install nvidia driver.

#1 You can change  UUI /boot/grub/grub.cfg
e.g. F:\boot\grub\grub.cfg (F is my USB). Add parameter nouveau.modeset=0 under persistance section at the end of the line, after editation it should look like this:

    menuentry "Live system (persistence, check kali.org/prst)" {
    linux /live/vmlinuz-5.6.7-kali3-amd64 boot=live components splash username=root hostname=kali persistence nouveau.modeset=0
    initrd /live/initrd.img-5.6.7-kali3-amd64
**Note** select kali persistence to boot.

#2 Once you have that ready boot to your kali persistence.

    apt-get update && apt-get upgrade -y && apt-get dist-upgrade –y
    apt-get install linux-headers-$(uname -r) –y
    reboot
#3 Now you should see that Kali booted in to low resolution login screen, GOOD. log in and type in terminal:

**init 3** (will exit GUI and help nvidia drivers to install correctly)

    apt-get install -y ocl-icd-libopencl1 nvidia-driver nvidia-cuda-toolkit

Once this is done reboot and you should have USB bootable pendrive with NVIDIA drivers running.
You can verify that with nvidia-smi command, also I need to mention that this worked for me even without updating initramfs (update-initramfs.distrib -u).

## Post installation 

Ref.

[Post install for Live USB persistent](https://github.com/leonetolesano/custom-kali-tutorial/wiki/0x03-Post-install-for-Live-USB-persistent)

[The First 10 Things to Do After Installing Kali Linux](https://www.fossmint.com/things-to-do-after-installing-kali-linux/)

enjoy :)
