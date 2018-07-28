#!/usr/bin/env python

#gunicorn -c gunicorn_server.py app:app

bind = '127.0.0.1:5001'
workers = 4
worker_class = 'sync'
threads = 2
# logfile = '../log_file/gunicorn.log'
# loglevel = 'info'
