#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import click

import omnithumb
import asyncio
from omnithumb import default_settings
from omnithumb.conversion.utils import convert as async_convert
from omnithumb.types.typestring import TypeString

def get_config():
    from omnithumb.conversion.converter import ConverterGraph
    from omnithumb.responses.placeholder import PlaceholderSelector
    settings = default_settings
    custom_settings_path = os.environ.get('OMNIC_SETTINGS')
    if custom_settings_path:
        # TODO import here
        pass
    settings.converter_graph = ConverterGraph(settings.CONVERTERS)
    settings.placeholders = PlaceholderSelector(settings)
    return default_settings

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
    '''
    Runs a Omnic web server
    '''
    click.echo('Start server at: {}:{}'.format(ip, port))
    # TODO: add reloading, add environ 
    settings = get_config()
    omnithumb.runserver(settings, host=ip, port=port, debug=debug)

    #register_all()
    #app.run(host=ip, port=port, debug=debug)

@cmds.command()
@click.argument('file', required=True)
@click.argument('type', required=True)
def convert(file, type):
    '''
    Converts a single file to a given type
    '''
    path = file
    to_type = TypeString(type)
    if not path.startswith('/'):
        dirname = path.dirname(__file__)
        path = os.path.normpath(dirname, path)
    click.echo('Converting: {} -> {}'.format(path, to_type))
    settings = get_config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_convert(settings, path, to_type))
    loop.close()

def main():
    cmds()
