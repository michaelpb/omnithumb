from PIL import Image

from omnithumb.types.typestring import TypeString
from omnithumb.types.resource import TypedResource
from omnithumb.conversion import converter

class PILThumb(converter.Converter):
    inputs = [
        'JPG',
        'PNG',
        'GIF',
        'BMP',
        'image/jpg',
        'image/jpeg',
        'image/gif',
        'image/png',
        'image/bitmap',
    ]
    outputs = ['thumb.png']
    default_size = (200, 200)

    def generate_thumb(self, size, orig_resource, thumb_resource):
        with orig_resource.cache_open() as orig:
            im = Image.open(orig)
            im.thumbnail(size)
        with thumb_resource.cache_open('wb') as target:
            im.save(target, 'JPEG')

    async def convert(self, in_resource, out_resource):
        size = self.default_size
        arguments = out_resource.typestring.arguments
        if arguments:
            width_s, _, height_s = arguments[0].partition('x')
            size = (int(width_s), int(height_s))
        self.generate_thumb(size, in_resource, out_resource)

