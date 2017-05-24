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

#@blueprint.route('/<width:int>x<height:int>/<url_suffix:.+>')
#async def thumb_route(request, width, height, url_suffix):

PIXEL_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
PIXEL_B = b64decode(PIXEL_B64)

async def stream_pixel(response):
    response.write(PIXEL_B)

async def generate_thumb(size, orig_resource, thumb_resource):
    print('generating thumb', size)
    with orig_resource.open('rb') as orig:
        im = Image.open(orig)
        im.thumbnail(size)
        with thumb_resource.open('wb') as target:
            print('saved to ', thumb_resource.cache_path)
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
        return await response.file(thumb_resource.cache_path)

    # Check if original resource exists
    orig_resource = utils.Resource(config, url_string)
    if not orig_resource.cache_exists():
        print('queue up downloading original')
        Service.app.loop.create_task(orig_resource.download())
    # Generate original resource
    print('queue up generating thumb')
    task = generate_thumb((width, height), orig_resource, thumb_resource)
    Service.app.loop.create_task(task)

    # Respond with placeholder
    return response.stream(stream_pixel, content_type='image/png')

