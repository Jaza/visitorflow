#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 3 ] || die "The listen.sh script has three required arguments: tshark_timeout, wlan_interface, and log_db, e.g: ./listen.sh 3600 wlan0 /tmp/tshark.db"

sqlite3 $2 "CREATE TABLE IF NOT EXISTS tshark_log (id INTEGER PRIMARY KEY, line TEXT);"

timeout $1 stdbuf -oL tshark -i $2 -I -f 'broadcast' -R 'wlan.fc.type == 0 && wlan.fc.subtype == 4' -T fields -e frame.time_epoch -e wlan.sa -e radiotap.dbm_antsignal | (while read line; do sqlite3 $3 "INSERT INTO tshark_log (line) VALUES ('$line');"; done) > /dev/null 2>&1
