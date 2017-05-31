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

def enqueue_conversion_path(url_string, to_type):
    config = ServiceMeta.config
    target_ts = TypeString(str(to_type))
    foreign_res = ForeignResource(config, url_string)

    # Determine the file type of the foreign resource
    typed_foreign_res = foreign_res.guess_typed()

    if not typed_foreign_res.cache_exists():
        # Symlink to new location that includes typed extension
        typed_foreign_res.symlink_from(foreign_res)

    # Now find path between types
    original_ts = typed_foreign_res.typestring
    path = config.converter_graph.find_path(original_ts, target_ts)

    # Loop through each step in graph path and convert
    for converter_class, from_ts, to_ts in path:
        converter = converter_class(config)
        in_resource = TypedResource(config, url_string, from_ts)
        out_resource = TypedResource(config, url_string, to_ts)
        ServiceMeta.enqueue_convert(converter, in_resource, out_resource)

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

    # Check if the original resource is already downloaded, if not
    # enqueue the download of that
    foreign_res = ForeignResource(config, url_string)
    if not foreign_res.cache_exists():
        ServiceMeta.enqueue_download(foreign_res)

    # Enqueue a single function that will in turn enqueue the remaining
    # conversion process
    ServiceMeta.enqueue_sync(enqueue_conversion_path, url_string, target_ts)
    return config.placeholders.stream_response(target_ts, response)

