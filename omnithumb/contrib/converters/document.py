from omnithumb.types.typestring import TypeString
from omnithumb.types.resource import TypedResource
from omnithumb.conversion import converter

class Unoconv(converter.ExecConverter):
    inputs = [
        # Document
        'BIB',
        'DOC',
        'HTML',
        'XHTML',
        'HTM',
        'ODT',
        'OTT',
        'RTF',
        'LTX',
        'SDW',
        'STW',
        'SXW',
        'TXT',
        'UOT',
        'VOR',

        # Spreadsheet
        'CSV',
        'XLS',
        'DBF',
        'ODS',
        'XML',

        # Presentation
        'ODP',
        'PPT',
        'PPTX',

        'application/msword',
        'application/vnd.oasis.opendocument.text',
        # TODO: remove this
        #'application/octet-stream',
    ]

    outputs = [
        'PDF',
        'application/pdf',
    ]

    command = [
        # TODO fix running unoconv within venv
        '/usr/bin/python3',
        '/usr/bin/unoconv',
        '-f',
        '$0',
        '-o',
        '$OUT',
        '$IN',
    ]

    def get_arguments(self, out_resource):
        return [out_resource.typestring.extension.lower()]

class ImageMagickPageRasterizer(converter.ExecConverter):
    inputs = [
        # Document
        'PDF',
        'PS',
        'application/pdf',
        'application/postscript',
    ]

    outputs = [
        'PNG',
        'image/png',
    ]

    command = [
        'convert',
        '$IN',
        '$OUT',
    ]
