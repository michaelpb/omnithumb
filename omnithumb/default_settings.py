from omnithumb.contrib.converters.thumb import PILThumb
#from omnithumb.contrib.placeholders import PNGPixel

SERVICES = [
    'omnithumb.contrib.services.media',
]

CONVERTERS = [
    PILThumb,
]


PLACEHOLDERS = [
    #PNGPixel,
]

PATH_PREFIX = '/tmp/omnithumb/'
PATH_GROUPING = 'MD5'
ALLOWED_LOCATIONS = {'localhost:8080', 'placehold.it', 'unsplash.it'}
