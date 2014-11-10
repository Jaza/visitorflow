#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}
[ "$#" -eq 1 ] || die "Path to and arguments for listen.py script required, e.g: ./listen_and_reboot.sh ~/listen.py http://192.168.1.1/agent/report/ "$(cat /sys/class/net/wlan0/address)" wlan0 /tmp/tshark.log"
sleep 15
eval $1
sudo /sbin/reboot
