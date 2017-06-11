from omnithumb.contrib.converters.thumb import PILThumb
from omnithumb.contrib.converters.document import Unoconv, ImageMagickPageRasterizer
from omnithumb.contrib.converters.mesh import MeshLabConverter, Jsc3dRenderer
from omnithumb.contrib.converters.chemical import OpenBabelConverter
from omnithumb.contrib.converters.vector import InkscapeConverter, InkscapeRasterizer
from omnithumb.contrib.responses.placeholders import PNGPixel

# Set up logging format
import logging
logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG
)

SERVICES = [
    'omnithumb.contrib.services.media',
    'omnithumb.contrib.services.test',
]

CONVERTERS = [
    PILThumb,
    Unoconv,
    ImageMagickPageRasterizer,
    MeshLabConverter,
    Jsc3dRenderer,
    OpenBabelConverter,
    InkscapeConverter,
    InkscapeRasterizer,
]

class CatchAll(PNGPixel):
    types = all

PLACEHOLDERS = [
    PNGPixel,
    CatchAll,
]

PATH_PREFIX = '/tmp/omnithumb/'
PATH_GROUPING = 'MD5'
ALLOWED_LOCATIONS = {'localhost:8080', 'placehold.it', 'unsplash.it'}
