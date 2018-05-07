from picker import *

opts = Picker(
    title = 'COMMITS',
    options = [
        ".autofsck", ".autorelabel", "bin/", "boot/", 
        "cgroup/", "dev/", "etc/", "home/", "installimage.conf",
        "installimage.debug", "lib/", "lib64/", "lost+found/",
        "media/", "mnt/", "opt/", "proc/", "root/",
        "sbin/", "selinux/", "srv/", "sys/",
        "tmp/", "usr/", "var/"
    ]
).getSelected()

if opts == False:
    print "Aborted!"
else:
    print opts
