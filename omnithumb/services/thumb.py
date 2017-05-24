from base64 import b64decode

from PIL import Image

from sanic.response import json
from sanic import Blueprint
from sanic import response
from sanic import Sanic

from .. import utils

class Service:
    NAME = 'thumb'
    blueprint = Blueprint(NAME)
    config = None
    app = None
    log = None
    enqueue = None

#@blueprint.route('/<width:int>x<height:int>/<url_suffix:.+>')
#async def thumb_route(request, width, height, url_suffix):

PIXEL_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
PIXEL_B = b64decode(PIXEL_B64)

async def stream_pixel(response):
    response.write(PIXEL_B)

def generate_thumb(size, orig_resource, thumb_resource):
    Service.log.debug('generating thumb ' + repr(size))
    with orig_resource.open_cache() as orig:
        try:
            im = Image.open(orig)
        except Exception as e:
            Service.log.warning('Error opening: ' + repr(e))
            return
        im.thumbnail(size)
    with thumb_resource.open_cache('wb') as target:
        Service.log.debug('Saved to ' + thumb_resource.cache_path)
        im.save(target, 'JPEG')

@Service.blueprint.get('/')
async def thumb_route(request):
    config = Service.config
    width = int(request.args['width'][0])
    height = int(request.args['height'][0])
    url_suffix = request.args['url'][0]
    url_string = 'http://' + url_suffix
    prefix = 'thumb-%ix%i' % (width, height)
    thumb_resource = utils.Resource(config, url_string, prefix)

    # Send back cache if it exists
    if thumb_resource.cache_exists():
        return await response.file(thumb_resource.cache_path, headers={
                'Content-Type': 'image/jpeg',
            })

    # Check if original resource exists, enqueue download if not
    orig_resource = utils.Resource(config, url_string)
    if not orig_resource.cache_exists():
        Service.log.debug('queue up downloading original')
        Service.enqueue(orig_resource.download)

    # Generate original resource
    Service.log.debug('queue up generating thumb')
    Service.enqueue(generate_thumb, (width, height), orig_resource, thumb_resource)

    # Respond with placeholder
    return response.stream(stream_pixel, content_type='image/png')

