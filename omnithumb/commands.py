#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import click

import omnithumb
from omnithumb import default_settings as settings
from omnithumb.converter.utils import convert as async_convert
from omnithumb.types.typestring import TypeString

def get_config():
    extra_settings = os.environ.get('OMNIC_SETTINGS')
    if extra_settings:
        # TODO import here
        pass

@click.group()
def cmds():
    pass

@cmds.command()
@click.option('--port', default=os.environ.get('PORT', 8080), type=int,
              help=u'Set application server port')
@click.option('--ip', default=os.environ.get('HOST', 'localhost'), type=str,
              help=u'Set application server ip')
@click.option('--debug', default=False,
              help=u'Set application server debug')
def runserver(port, ip, debug):
    click.echo('Start server at: {}:{}'.format(ip, port))
    # TODO: add reloading, add environ 
    omnithumb.runserver(settings, host=ip, port=port, debug=debug)

    #register_all()
    #app.run(host=ip, port=port, debug=debug)

@cmds.command()
@click.argument('file', required=True)
@click.argument('type', required=True)
def convert(path, to_type):
    # TODO: add running of tests
    if not path.startswith('/'):
        dirname = path.dirname(__file__)
        path = os.path.resolve(dirname, path)
    to_type = TypeString(path)
    asyncio.ensure_future(async_convert(path, to_type))

def main():
    cmds()
