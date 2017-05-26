from omnithumb.old_utils import Type
#from omnithumb.thumb import ThumbType

SERVICES = [
    'omnithumb.services.thumb',
    'omnithumb.services.media',
]

# TODO Define various types
TYPES = [
]

# TODO Define how to get from type A to type B, which is used to create a
# directed graph of all types
PIPELINES = [
    'omnithumb.pipelines.thumb',
]

PATH_PREFIX = '/tmp/omnithumb/'
PATH_GROUPING = 'MD5'
ALLOWED_LOCATIONS = {'localhost:8080', 'placehold.it', 'unsplash.it'}
