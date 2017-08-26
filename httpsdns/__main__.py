#!/usr/bin/env python
# -*- coding:utf8 -*-

import argparse
import sys
import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems

import config
from httpsdns.utils.logger import logger

## init logger https://github.com/senko/python-logger/blob/master/logger.py
logger.basicConfig()

class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        options_simple = {
            'bind': '%s:%s' % (config.FLASK_HOST, config.FLASK_PORT),
            'workers': ((multiprocessing.cpu_count() * 2) + 1)
        }
        self.options = options or options_simple
        self.application = app
        super(StandaloneApplication, self).__init__()
    
    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
            if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def parse():
    parser = argparse.ArgumentParser(description="Https-DNS using google https dns")
    parser.add_argument("arg", help="python -m httpsdns run")
    return parser.parse_args()

def main():
    args = parse()
    if args.arg == "run":
        logger.debug('Begin Runing')
        from httpsdns.app import app as app
        app.run(config.FLASK_HOST, config.FLASK_PORT)
    elif args.arg == "gunicorn":
        logger.debug('Gunicorn MODE Begin Runing')
        from httpsdns.app import app as app
        StandaloneApplication(app).run()


if __name__ == '__main__':
    main()
