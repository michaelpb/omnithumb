from omnithumb.contrib.converters.thumb import PILThumb
from omnithumb.contrib.converters.document import Unoconv, ImageMagickPageRasterizer
from omnithumb.contrib.responses.placeholders import PNGPixel

SERVICES = [
    'omnithumb.contrib.services.media',
]

CONVERTERS = [
    PILThumb,
    Unoconv,
    ImageMagickPageRasterizer,
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
