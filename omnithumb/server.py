from sanic import Sanic

import logging
import importlib
import uvloop
import asyncio

from omnithumb.worker import AioWorker
from omnithumb.worker import Task

app = None

def register_service(settings, service):
    service.config = settings
    service.app = app
    app.blueprint(service.blueprint, url_prefix='/%s' % service.NAME)
    service.log = logging.getLogger()

    def enqueue_sync(func, *func_args):
        args = (func,) + func_args
        coro = settings.worker.enqueue(Task.FUNC, args)
        asyncio.ensure_future(coro)
    service.enqueue_sync = enqueue_sync

    def enqueue_download(resource):
        coro = settings.worker.enqueue(Task.DOWNLOAD, (resource,))
        asyncio.ensure_future(coro)
    service.enqueue_download = enqueue_download

    def enqueue_convert(converter, from_resource, to_resource):
        args = (converter, from_resource, to_resource)
        coro = settings.worker.enqueue(Task.CONVERT, args)
        asyncio.ensure_future(coro)
    service.enqueue_convert = enqueue_convert

def register_all(settings, services):
    for service_name in services:
        service = importlib.import_module(service_name)
        register_service(settings, service.ServiceMeta)


def runserver(settings, host, port, debug=False, just_setup_app=False):
    # Only import if actually running server (so that Sanic is not a dependency
    # if only using for convert mode)
    global app
    app = Sanic(__name__)
    register_all(settings, settings.SERVICES)

    # Set up loop + queue
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    settings.async_queue = asyncio.Queue(loop=loop)
    settings.worker = AioWorker(settings.async_queue)

    if just_setup_app: # in unit tests likely, don't make the coroutines
        return app

    # Start server and worker
    server_coro = app.create_server(host=host, port=port, debug=debug)
    worker_coro = settings.worker.run()
    loop.run_until_complete(asyncio.gather(server_coro, worker_coro))

    return app

