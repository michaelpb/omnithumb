from base64 import b64decode

from PIL import Image

from sanic import Blueprint
from sanic import response
from sanic import Sanic

from omnithumb.types.typestring import TypeString
from omnithumb.types.resource import TypedResource, ForeignResource

class ServiceMeta:
    NAME = 'media'
    blueprint = Blueprint(NAME)
    config = None
    app = None
    log = None
    enqueue = None

def process_media_route(url_string, to_type):
    config = ServiceMeta.config
    target_ts = TypeString(str(to_type))
    foreign_res = ForeignResource(config, url_string)

    if not foreign_res.cache_exists():
        # TODO: make awaitable
        foreign_res.download()

    # Determine the file type of the foreign resource
    typed_foreign_res = foreign_res.guess_typed()

    if not typed_foreign_res.cache_exists():
        # Symlink to new location that includes typed extension
        typed_foreign_res.symlink_from(foreign_res)

    # Now find path between types
    original_ts = typed_foreign_res.typestring
    path = config.converter_graph.find_path(original_ts, target_ts)

    # TODO: make each conversion a separate task
    # Loop through each step in graph path and convert
    for converter_class, from_ts, to_ts in path:
        converter = converter_class(config)
        in_resource = TypedResource(config, url_string, from_ts)
        out_resource = TypedResource(config, url_string, to_ts)
        converter.convert(in_resource, out_resource)


@ServiceMeta.blueprint.get('/<ts>/')
async def media_route(request, ts):
    config = ServiceMeta.config
    url_suffix = request.args['url'][0]
    url_string = 'http://' + url_suffix

    target_ts = TypeString(ts)
    target_resource = TypedResource(config, url_string, target_ts)

    # Send back cache if it exists
    if target_resource.cache_exists():
        return await response.file(target_resource.cache_path, headers={
                'Content-Type': target_ts.mimetype,
            })

    #ServiceMeta.enqueue(process_media_route, url_string, target_ts)
    process_media_route(url_string, target_ts)

    # TODO: Convert to a Placeholder
    PIXEL_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
    PIXEL_B = b64decode(PIXEL_B64)

    async def stream_pixel(response):
        response.write(PIXEL_B)

    # Respond with placeholder
    return response.stream(stream_pixel, content_type='image/png')

    # TODO:
    return config.placeholders.stream_response(response, target_ts)




