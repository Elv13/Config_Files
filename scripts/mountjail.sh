#!/bin/sh

if [ "$1" == "" ]; then
    exit 1
fi

sudo mount -o bind /dev/ $1/dev/
sudo mount -o bind /dev/pts $1/dev/pts
sudo mount -o bind /proc $1/proc
sudo mount -o bind /sys $1/sys
sudo cp /etc/resolv.conf $1/etc/
sudo chroot $1 /bin/bash
