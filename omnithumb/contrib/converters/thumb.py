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
    ]
    outputs = [
        'thumb.png',
        'thumb.jpg',
    ]
    default_size = (200, 200)

    def generate_thumb(self, size, orig_resource, thumb_resource):
        with orig_resource.cache_open() as orig:
            im = Image.open(orig)
            im.thumbnail(size)
        with thumb_resource.cache_open('wb') as target:
            if thumb_resource.typestring.ts_format == 'thumb.jpg':
                # Ensure it has no alpha before saving
                if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
                    alpha = im.convert('RGBA').split()[-1]
                    no_alpha = Image.new("RGB", im.size, (255, 255, 255))
                    no_alpha.paste(im, mask=alpha)
                    no_alpha.save(target, 'JPEG')
                else:
                    im.save(target, 'JPEG')
            else:
                # Save as is
                im.save(target)

    async def convert(self, in_resource, out_resource):
        size = self.default_size
        arguments = out_resource.typestring.arguments
        if arguments:
            width_s, _, height_s = arguments[0].partition('x')
            size = (int(width_s), int(height_s))
        self.generate_thumb(size, in_resource, out_resource)

