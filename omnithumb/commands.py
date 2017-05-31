#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import click

import omnithumb
from omnithumb import default_settings as settings

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
    omnithumb.runserver(settings, host=ip, port=port, debug=debug)

    register_all()
    # TODO: add reloading, add environ 
    app.run(host=ip, port=port, debug=debug)

@cmds.command()
def test():
    # TODO: add running of tests
    pass

def main():
    cmds()

if __name__ == "__main__":
    cmds()
