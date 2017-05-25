
'''
Two types:
- Converters (a -> b)
- Optimizers (a -> OptimizeA)
'''

_eg_conversion_command = '''
'''

class ImageMagickRasterizerConverter(Converter):
    inputs = [
        'application/pdf',
        'image/svg',
    ]

    output = 'image/png'

    cost = 5

    CMD = [
        'convert',
            '-verbose',
            '-density', '150',
            '-trim',
            '$INPUT',
            '-quality', '100',
            '-flatten',
            '-sharpen', '0x1.0',
            '$OUTPUT',
    ]

class InkscapeConverter(Converter):
    inputs = [
        'svgz',
        'dia',
        'ai',
        'wpf',
        'wpm',
        'sk1',
        'plt',
        'outline',
    ]
    cost = 10

    output = 'svg'

    CMD = [
        'inkscape',
            '-z',
            '-f', '$INPUT',
            '-e', '$OUTPUT',
    ]


class UnoConvConverter(Converter):
    inputs = [
        'odt',
        'odg',
        'odp',
        'odf',
        'pptx',
        'ppt',
        'doc',
        'docx',
        'rtf',
    ]
    output = 'application/pdf'
    cost = 20
    CMD = [
        'unoconv',
            '-f', '$INPUT',
            '$OUTPUT',
    ]


class MeshLabConverter(Converter):
    inputs = [
        'obj',
        'stl',
        '3ds',
        'ptx',
        'ply',
        'dae',
    ]

    output = 'stl'

    cost = 5

    CMD = [
        'convert',
            '-verbose',
            '-density', '150',
            '-trim',
            '$INPUT',
            '-quality', '100',
            '-flatten',
            '-sharpen', '0x1.0',
            '$OUTPUT',
    ]


class ThumbOptimizer(Optimizer):
    prefered_input = [
        'image/png'
        'image/jpeg'
    ]

    cost = 1

    inputs = [
        'image/cgm',
        'image/gif',
        'image/ief'
        'image/jpeg',
        'image/pcx',
    ]

    output = ThumbType

    def convert(in_resource, out_resource):
        with in_resource.open_cache() as orig:
            im = Image.open(orig)
            im.thumbnail(size)
        with out_resource.open_cache('wb') as target:
            im.save(target, 'JPEG')

