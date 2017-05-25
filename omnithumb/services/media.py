from sanic.response import json
from sanic import Blueprint
from sanic import response
from sanic import Sanic

from .. import utils

class Service:
    NAME = 'media'
    blueprint = Blueprint(NAME)
    config = None
    app = None
    log = None
    enqueue = None

@Service.blueprint.get('/')
async def media(request):
    pass


@blueprint.route('/<typestring>/<url_shortener>/<url_fragment>')
async def media_shortened(request, typestring, url_shortener, url_fragment):
    # TODO: In configuration, define shorteners like "gh" (for github), which
    # take an url_fragment (could even substitute "/" for some other char, like
    # ",") and output an absolute URL
    pass




