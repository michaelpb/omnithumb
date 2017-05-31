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
        # TODO: remove this
        'application/octet-stream',
    ]

    outputs = [
        'PDF',
        'application/pdf',
        'PNG',
        'image/png',
    ]

    command = [
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
