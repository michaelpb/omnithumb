#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import click

from sanic import Sanic

app = Sanic(__name__)

def register_service(service):
    service.config = None
    service.app = app
    app.blueprint(service.blueprint, url_prefix='/%s' % service.NAME)

def register_all():
    from omnithumb.services import thumb
    register_service(thumb.Service)

@click.group()
def cmds():
    pass

@cmds.command()
@click.option('--port', default=os.environ.get('PORT', 8080), type=int,
              help=u'Set application server port!')
@click.option('--ip', default=os.environ.get('HOST', 'localhost'), type=str,
              help=u'Set application server ip!')
@click.option('--debug', default=False,
              help=u'Set application server debug!')
def runserver(port, ip, debug):
    click.echo('Start server at: {}:{}'.format(ip, port))
    register_all()
    # TODO: add reloading, add environ 
    app.run(host=ip, port=port, debug=debug)


@cmds.command()
def test():
    # TODO: add running of tests
    pass

if __name__ == "__main__":
    cmds()
