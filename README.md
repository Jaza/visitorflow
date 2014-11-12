Visitor Flow
============

Django app and Python script to record wifi monitoring logs for analytics purposes.

Original app built for the Indianapolis Museum of Art (IMA), article explaining it at: http://mw2013.museumsandtheweb.com/paper/3817/

This repo forked from the original: https://github.com/IMAmuseum/visitorflow

Usage
-----

1.  Make sure you have MySQL (including dev libraries, and MySQLdb for Python) installed on the endpoint server, and make sure you have sqlite3 (including the Python library) installed on the client device (e.g. Raspberry Pi).
2.  Clone the visitorflow repo to the endpoint server:

    ```
    git clone https://github.com/Jaza/visitorflow.git
    cd visitorflow
    ```

3.  (Optional but recommended). Set up a (Python 2.7) virtualenv (recommended to use with '--system-site-packages option') and activate it, e.g:

    ```
    virtualenv --system-site-packages .
    source bin/activate
    ```

4.  Install dependencies:

    ```
    pip install -r requirements.txt
    ```

5.  Create writable log directory:

    ```
    mkdir log
    chmod 777 log
    ```

6.  Make manage.py executable:

    ```
    chmod a+x project/manage.py
    ```

7.  Set up an empty database and a database user for the app.
8.  Copy the project/settings/example_local_settings.py to project/settings/local_settings.py, and edit local_settings.py per your setup.
9.  Install database schema:

    ```
    ./project/manage.py migrate
    ```

10. Copy the wsgi/example_wsgi.py to wsgi/local_wsgi.py, and edit local_wsgi.py per your setup.
11. Set up your webserver to serve the site via the local_wsgi.py file (e.g. create an Apache VirtualHost that calls it from a subdomain).
12. Set the 'normalizeSightings' script to run regularly (e.g. every 5 minutes) via a cron job:

    ```
    /path/to/python /path/to/project/manage.py normalizeSightings
    ```

13. Copy the scripts/listen.sh and scripts/listen_if_notrunning.sh files to the client device (e.g. Raspberry Pi), and set something like this to run regularly (e.g. every 5 minutes) via a cron job:

    ```
    /path/to/listen_if_notrunning.sh "/path/to/listen.sh wlan0 /path/to/tshark.db"
    ```

14. Copy the scripts/send.py and scripts/send_if_notrunning.sh files to the client device (e.g. Raspberry Pi), and set something like this to run regularly (e.g. every 5 minutes) via a cron job:

    ```
    /path/to/send_if_notrunning.sh "/path/to/send.py http://endpoint.server.url/agent/report/ "$(echo -n "$(cat /sys/class/net/wlan0/address)" | openssl sha1 -hmac "key" | sed 's/^.* //')" wlan0 /path/to/tshark.db 1000 endpoint_username:endpoint_password"
    ```
