#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}
[ "$#" -eq 1 ] || die "Path to and arguments for listen.sh script required, e.g: ./listen_if_notrunning.sh ~/listen.sh wlan0 /tmp/tshark.db"
result=`ps aux | grep -i "listen.sh" | grep -v "grep" | grep -v "listen_if_notrunning" | wc -l`
if [ $result -eq 0 ]
then
  eval $1
fi
