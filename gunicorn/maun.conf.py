# esr21 gunicorn.conf
import os

SOURCE_ROOT = os.path.expanduser('~/source')

errorlog = os.path.join(
    SOURCE_ROOT, 'esr21/logs/esr21-maun-gunicorn-error.log')
accesslog = os.path.join(
    SOURCE_ROOT, 'esr21/logs/esr21-maun-gunicorn-access.log')
loglevel = 'debug'
pidfile = os.path.join(SOURCE_ROOT, 'esr21/logs/esr21-maun.pid')

workers = 2  # the number of recommended workers is '2 * number of CPUs + 1'

raw_env = ['DJANGO_SETTINGS_MODULE=esr21.community.maun']

bind = "127.0.0.1:9011"
