#!/usr/bin/env python
from __future__ import print_function

import sys
import os
import subprocess
import time
import re
import hashlib
import socket
import urllib
import urllib2


def main_loop(server_endpoint, host_identifier, wlan_interface, log_file):
    # Remove the log file if present
    try:
        os.unlink(log_file)
        print("deleted log")
    except:
        print("no log to delete")
        pass
    # start the tshark process, outputting to file
    print("opening process")
    proc = subprocess.Popen("stdbuf -oL tshark -i %s -I -f 'broadcast' -R 'wlan.fc.type == 0 && wlan.fc.subtype == 4' -T fields -e frame.time_epoch -e wlan.sa -e radiotap.dbm_antsignal > %s" % (
        wlan_interface,
        log_file)
    ,
        shell=True,
        bufsize=1,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    # give the process a few seconds to open its log file
    print("sleeping...")
    time.sleep(3)
    # open the log file
    log = open(log_file, 'r+')
    print("log opened")
    sightings = []
    try:
        # start process loop
        while (True):
            # report any sightings
            report(sightings, server_endpoint, host_identifier)
            # read in one line of log
            line = log.readline()
            # empty string is sent back if no input available
            if line == "":
                # is the process dead? if so stop reading log
                if proc.poll() is not None:
                    print("process died")
                    break
                # wait a second so we aren't hammering the log file
                time.sleep(1)
            else:
                # see if the input line matches our expected format
                match = re.search(r"(\d+)\.\d+\t([a-z0-9:]+)\t([0-9-]+)\n", line)
                if match is not None:
                    sightings.append(match.groups())
    except KeyboardInterrupt:
        clean_up(proc, log)
        print("exited by command")
        sys.exit()
    # clean up
    clean_up(proc, log)


def report(sightings, server_endpoint, host_identifier):
    # if there are any sightings queued for reporting, send to server
    for index in range(len(sightings)):
        sighting = sightings[index]
        data = {
            'host': host_identifier,
            'timestamp': sighting[0],
            'device_id': hashlib.sha1(sighting[1]).hexdigest(),
            'signal_dbm': sighting[2]
        }
        del sightings[index]
        # don't crash if the request fails
        try:
            req = urllib2.urlopen(server_endpoint, urllib.urlencode(data))
            req.close()
        except:
            print('Request to server endpoint %s with data %s failed' % (server_endpoint, data), file=sys.stderr)
            pass


def clean_up(proc, log):
    try:
        proc.terminate()
        proc.poll()
    except:
        pass
    log.close()


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Four arguments are required for this script: server_endpoint, host_identifier, wlan_interface, and log_file; e.g. ./listen.py http://192.168.1.1/agent/report/ "$(cat /sys/class/net/wlan0/address)" wlan0 /tmp/tshark.log', file=sys.stderr)
        sys.exit(1)

    # start main loop
    while (True):
        main_loop(
            server_endpoint=sys.argv[1],
            host_identifier=sys.argv[2],
            wlan_interface=sys.argv[3],
            log_file=sys.argv[4])
