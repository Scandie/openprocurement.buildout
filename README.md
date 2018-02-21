# openprocurement.buildout
Development Buildout of OpenProcurement

Follow the instructions:

  1. Bootstrap the buildout with Python 2.7:

     ```
     $ python bootstrap.py
     ```

  2. Build the buildout:

      ```
      $ bin/buildout -N
      ```

System requirements (fedora 22):

    dnf install gcc file git libevent-devel python-devel sqlite-devel zeromq-devel libffi-devel openssl-devel systemd-python

Local development environment also requires additional dependencies:

    dnf install couchdb

To start environment services:

    bin/circusd --daemon

To run openprocurement.api instance:

    bin/pserve etc/openprocurement.api.ini

To run tests:

    bin/python run_tests.py
    
To print packages that will be tested to console:

    bin/python run_tests.py --list-packages
    
To specify groups of packages that should be tested:

    bin/python run_tests.py openprocurement
