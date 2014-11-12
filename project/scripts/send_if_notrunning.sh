#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}
[ "$#" -eq 1 ] || die "Path to and arguments for send.py script required, e.g: ./send_if_notrunning.sh ~/send.py http://192.168.1.1/agent/report/ \"\$(echo -n \"\$(cat /sys/class/net/wlan0/address)\" | openssl sha1 -hmac \"key\" | sed 's/^.* //')\" wlan0 /tmp/tshark.db 1000 endpoint_username:endpoint_password"
result=`ps aux | grep -i "send.py" | grep -v "grep" | grep -v "send_if_notrunning" | wc -l`
if [ $result -eq 0 ]
then
  sleep 15
  eval $1
fi
