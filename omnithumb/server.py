from sanic import Sanic
import logging
import importlib

from . import utils

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)

app = None

type_graph = utils.DirectedGraph()
type_graph.add_edge('image', 'thumb.500x500')

def register_service(settings, service):
    service.config = settings
    service.app = app
    app.blueprint(service.blueprint, url_prefix='/%s' % service.NAME)
    service.log = logging.getLogger()

    async def queued_task(func, *args):
        try:
            func(*args)
        except:
            service.log.error('Error in task %s: "%s"' %
                (service.NAME, repr(e)))

    def enqueue(func, *args):
        # TODO: replace with proper queue
        # Remove from "locked" set
        app.loop.create_task(queued_task(func, *args))

    def enqueue_type(orig_resource):
        if not orig_resource.cache_exists():
            enqueue(enqueue_download)
            enqueue_type(enqueue_download)
            return
        app.loop.create_task(queued_task(func, *args))

    def enqueue_download(orig_resource):
        service.log.debug('Queueing up downloading original')
        service.enqueue(orig_resource.download)

    service.enqueue = enqueue
    service.enqueue_download = enqueue_download
    service.enqueue_type = enqueue_type

def register_all(settings, services):
    for service_name in services:
        service = importlib.import_module(service_name)
        register_service(settings, service.Service)


def runserver(settings, host, port, debug=False):
    global app
    app = Sanic(__name__)
    register_all(settings, settings.SERVICES)
    app.run(host=host, port=port, debug=debug)
    return app

