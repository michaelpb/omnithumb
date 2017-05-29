from sanic import Sanic
import logging
import importlib


from omnithumb.types.converter import ConverterGraph
from omnithumb.responses.placeholder import PlaceholderSelector

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)

app = None

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

    service.enqueue = enqueue

def register_all(settings, services):
    for service_name in services:
        service = importlib.import_module(service_name)
        register_service(settings, service.ServiceMeta)


def runserver(settings, host, port, debug=False):
    global app
    app = Sanic(__name__)
    register_all(settings, settings.SERVICES)
    settings.converter_graph = ConverterGraph(settings.CONVERTERS)
    settings.placeholders = PlaceholderSelector(settings)
    app.run(host=host, port=port, debug=debug)
    return app

