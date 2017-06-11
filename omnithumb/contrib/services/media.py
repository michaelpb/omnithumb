from base64 import b64decode

from PIL import Image

from sanic import Blueprint
from sanic import response
from sanic import Sanic

from omnithumb.types.typestring import TypeString
from omnithumb.types.resource import TypedResource, TypedForeignResource, ForeignResource
from omnithumb.conversion.utils import enqueue_conversion_path
from omnithumb.config import settings

class ServiceMeta:
    NAME = 'media'
    blueprint = Blueprint(NAME)
    config = None
    app = None
    log = None
    enqueue = None

@ServiceMeta.blueprint.get('/<ts>/')
async def media_route(request, ts):
    url_suffix = request.args['url'][0]
    url_string = 'http://' + url_suffix

    target_ts = TypeString(ts)
    target_resource = TypedResource(settings, url_string, target_ts)

    # Send back cache if it exists
    if target_resource.cache_exists():
        return await response.file(target_resource.cache_path, headers={
                'Content-Type': target_ts.mimetype,
            })

    # Check if the original resource is already downloaded, if not
    # enqueue the download of that
    foreign_res = ForeignResource(settings, url_string)
    if not foreign_res.cache_exists():
        ServiceMeta.enqueue_download(foreign_res)

    # Enqueue a single function that will in turn enqueue the remaining
    # conversion process
    ServiceMeta.enqueue_sync(
        enqueue_conversion_path,
        url_string,
        str(target_ts),
        ServiceMeta.enqueue_convert
    )
    return settings.placeholders.stream_response(target_ts, response)

