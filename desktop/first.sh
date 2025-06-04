#!/bin/bash
sudo raspi-config --expand-rootfs
sudo resize2fs /dev/mmcblk0p2
rm -f $HOME/Desktop/first.sh
sudo reboot
