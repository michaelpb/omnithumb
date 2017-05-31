from omnithumb.contrib.converters.thumb import PILThumb
from omnithumb.contrib.converters.document import Unoconv
from omnithumb.contrib.responses.placeholders import PNGPixel

SERVICES = [
    'omnithumb.contrib.services.media',
]

CONVERTERS = [
    PILThumb,
    Unoconv,
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
