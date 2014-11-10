Visitor Flow
============

Django app and Python script to record wifi monitoring logs for analytics purposes.

Original app built for the Indianapolis Museum of Art (IMA), article explaining it at: http://mw2013.museumsandtheweb.com/paper/3817/

This repo forked from the original: https://github.com/IMAmuseum/visitorflow

Usage
-----

1.  Make sure you have installed:

    - MySQL (including dev libraries, and MySQLdb for Python)

2.  Clone the visitorflow repo:
    -
        git clone https://github.com/Jaza/visitorflow.git
        cd visitorflow
3.  Set up a (Python 2.7) virtualenv (recommended to use with '--system-site-packages option') and activate it, e.g:
    -
        virtualenv --system-site-packages .
        source bin/activate
4.  Install dependencies:
    -
        pip install -r requirements.txt
5.  Create writable log directory:
    -
        mkdir log
        chmod 777 log
6.  Make manage.py executable:
    -
        chmod a+x project/manage.py
7.  Set up an empty database and a database user for the app.
8.  Copy the project/settings/example_local_settings.py to project/settings/local_settings.py, and edit local_settings.py per your setup.
9.  Install database schema:
    -
        ./project/manage.py migrate
10. Copy the wsgi/example_wsgi.py to wsgi/local_wsgi.py, and edit local_wsgi.py per your setup.
