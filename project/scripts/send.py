#!/usr/bin/env python
from __future__ import print_function

import json
import sys
import os
import subprocess
import time
import re
import hashlib
import requests
import sqlite3


def main_loop(server_endpoint, host_identifier, wlan_interface, log_db, max_lines_per_request, wait_seconds_between_requests, endpoint_auth):
    try:
        # start process loop
        while (True):
            time.sleep(int(wait_seconds_between_requests))
            sightings = []
            ids = []

            try:
                is_query_successful = False
                results = None

                while (not is_query_successful):
                    try:
                        conn = sqlite3.connect(log_db)
                        # read in one line of log
                        c = conn.execute('SELECT id, line FROM tshark_log ORDER BY id ASC LIMIT 0, ?', (max_lines_per_request,))
                        results = c.fetchall()
                        conn.close()
                        is_query_successful = True
                    except sqlite3.OperationalError:
                        # wait a second so we aren't hammering the log file
                        time.sleep(1)

                # see if the input lines match our expected format
                for id, line in results:
                    match = re.search(r"(\d+)\.\d+\t([a-z0-9:]+)\t([0-9-]+)\n?", line)
                    if match is not None:
                        sightings.append(match.groups())
                        ids.append(id)

                if len(ids):
                    # report any sightings
                    report(sightings, server_endpoint, host_identifier, endpoint_auth)

                    is_query_successful = False
                    while (not is_query_successful):
                        try:
                            conn = sqlite3.connect(log_db)
                            # delete processed log entries
                            c = conn.execute('DELETE FROM tshark_log WHERE id IN(%s)' % ', '.join('?'*len(ids)), ids)
                            conn.commit()
                            conn.close()
                            is_query_successful = True
                        except sqlite3.OperationalError:
                            # wait a second so we aren't hammering the log file
                            time.sleep(1)

            except TypeError:
                # wait a second so we aren't hammering the log file
                time.sleep(1)
    except KeyboardInterrupt:
        print("exited by command")
        sys.exit()


def report(sightings, server_endpoint, host_identifier, endpoint_auth):
    # if there are any sightings queued for reporting, send to server
    data = []
    for index in range(len(sightings)):
        sighting = sightings[index]
        data.append({
            'host': host_identifier,
            'timestamp': sighting[0],
            'device_id': hashlib.sha1(sighting[1]).hexdigest(),
            'signal_dbm': sighting[2]
        })

    if data:
        # don't crash if the request fails
        is_req_successful = False
        while (not is_req_successful):
            try:
                req = requests.post(server_endpoint, data=json.dumps({'sightings': data}), headers={'Connection':'close', 'content-type': 'application/json'}, auth=endpoint_auth, verify=False)
                if req and req.status_code == 200:
                    is_req_successful = True
            except:
                print('Request to server endpoint %s with data %s%s failed' % (server_endpoint, data, endpoint_auth and (' and auth %s' % endpoint_auth) or ''), file=sys.stderr)
                pass


if __name__ == '__main__':
    if len(sys.argv) < 7:
        print('Six arguments are required (and a seventh is optional) for this script: server_endpoint, host_identifier, wlan_interface, log_db, max_lines_per_request, wait_seconds_between_requests, and endpoint_auth; e.g. ./send.py http://192.168.1.1/agent/report/ "$(echo -n "$(cat /sys/class/net/wlan0/address)" | openssl sha1 -hmac "key" | sed \'s/^.* //\')" wlan0 /tmp/tshark.db 900 15 endpoint_username:endpoint_password', file=sys.stderr)
        sys.exit(1)

    # start main loop
    while (True):
        main_loop(
            server_endpoint=sys.argv[1],
            host_identifier=sys.argv[2],
            wlan_interface=sys.argv[3],
            log_db=sys.argv[4],
            max_lines_per_request=sys.argv[5],
            wait_seconds_between_requests=sys.argv[6],
            endpoint_auth=(len(sys.argv) > 7 and tuple(sys.argv[7].split(':')) or None))
