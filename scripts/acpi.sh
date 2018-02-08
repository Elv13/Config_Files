echo 'min_power' > '/sys/class/scsi_host/host0/link_power_management_policy'
echo '1500' > '/proc/sys/vm/dirty_writeback_centisecs'
echo '1' > '/sys/module/snd_hda_intel/parameters/power_save'
for I in `seq 1 5`;do echo 'min_power' > '/sys/class/scsi_host/host'${I}'/link_power_management_policy';done
echo 'auto' > '/sys/bus/usb/devices/1-1.3/power/control'
echo 'auto' > '/sys/bus/i2c/devices/i2c-0/device/power/control';
echo 'on' > '/sys/bus/usb/devices/1-1.5/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:14.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:16.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:19.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1a.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1b.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1c.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1c.2/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:03:00.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1c.4/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:00.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:01.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.3/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:03.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:01:00.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.2/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:02:00.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1d.0/power/control'
echo 'auto' > '/sys/bus/pci/devices/0000:00:1c.1/power/control'
ethtool -s enp0s25 wol d
echo 'auto' > '/sys/bus/usb/devices/1-1.6/power/control'
echo 'auto' > '/sys/bus/usb/devices/usb1/power/control'
echo 'auto' > '/sys/bus/usb/devices/usb2/power/control'
modprobe bbswitch
tee /proc/acpi/bbswitch <<<OFF
for I in `seq 0 7`; do echo powersave > /sys/devices/system/cpu/cpu${I}/cpufreq/scaling_governor;done

# block bluetooth
rfkill block 0
