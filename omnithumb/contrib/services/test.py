'''
Defines a service useful for writing unit tests or service availability
checks
'''
from sanic import Blueprint
from sanic import response
from sanic import Sanic

class ServiceMeta:
    NAME = 'test'
    blueprint = Blueprint(NAME)
    config = None
    app = None
    log = None
    enqueue = None

JPEG_TEST_BYTES = bytes([0xff, 0xd8, 0xff, 0xe0])
@ServiceMeta.blueprint.get('/test.jpg')
async def jpeg_route(request):
    async def streaming_fn(response):
        response.write(JPEG_TEST_BYTES)
    return response.stream(streaming_fn, content_type='image/jpeg')

PNG_TEST_BYTES = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
@ServiceMeta.blueprint.get('/test.png')
async def png_route(request):
    async def streaming_fn(response):
        response.write(JPEG_TEST_BYTES)
    return response.stream(streaming_fn, content_type='image/jpeg')

EMPTY_ZIP_TEST_BYTES = bytes([0x50, 0x4B, 0x05, 0x06])
@ServiceMeta.blueprint.get('/empty.zip')
async def zip_route(request):
    async def streaming_fn(response):
        response.write(EMPTY_ZIP_TEST_BYTES )
    return response.stream(streaming_fn, content_type='image/jpeg')

