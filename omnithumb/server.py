from sanic import Sanic
import logging
import importlib

logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)

app = None

def register_service(service):
    service.config = None
    service.app = app
    app.blueprint(service.blueprint, url_prefix='/%s' % service.NAME)
    service.log = logging.getLogger()

    # TODO add to swappable queue infrastructure
    async def queued_task(func, *args):
        try:
            func(*args)
        except:
            service.log.error('Error in task %s: "%s"' %
                (service.NAME, repr(e)))
    def enqueue(func, *args):
        app.loop.create_task(queued_task(func, *args))

    service.enqueue = enqueue

def register_all(services):
    for service_name in services:
        service = importlib.import_module(service_name)
        register_service(service.Service)

def runserver(settings, host, port, debug=False):
    global app
    app = Sanic(__name__)
    register_all(settings.SERVICES)
    app.run(host=host, port=port, debug=debug)
    return app


