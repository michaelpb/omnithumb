from omnithumb.conversion import converter

class MeshLabConverter(converter.ExecConverter):
    inputs = [
        # All 3D model formats and extensions supported by meshlabserver
        'OBJ',
        'MESH',
        'X3D',
        'X3DV',
        'X3DB',
        'OFF',
        '3DS',
        'PTX',
        'PLY',
        'DAE',
        'XYZ',
        'APTS',
        'PTS',
        'TRI',
        'ASC',
        'VRML',
        'ALN',
        'model/mesh',
        'model/vnd',
        'model/x3d',
        'model/vrml',
        'model/x3d+vrml',
        'model/x3d+xml',
        'model/x3d+binary',
        'application/postscript',
    ]

    outputs = [
        # Just convert everything into basic STL's for now
        'STL',
    ]

    command = [
        'meshlabserver',
        '-i',
        '$IN',
        '-o',
        '$OUT',
    ]


class Jsc3dRenderer(converter.ExecConverter):
    inputs = [
        'STL',
        'OBJ',
    ]

    outputs = [
        'PNG',
    ]

    command = [
        'jsc3d',
        '$IN',
        '$OUT',
    ]

class DimeConverter(converter.ExecConverter):
    # Uses DIME converter
    inputs = [
        'DXF',
        'image/vnd.dxf',
    ]

    outputs = [
        'VRML',
        'model/vrml',
    ]

    command = [
        'dxf2vrml',
        '$IN',
        '-o',
        '$OUT',
    ]

class KabejaAutocadConverter(converter.ExecConverter):
    # TODO Test
    # NOTE: Kabeja dies if there are spaces in the file name (yeap.... >_>),
    # need to add feature to converter base class to only have pretty/clean
    # filenames
    inputs = [
        'DXF',
        'image/vnd.dxf',
    ]

    outputs = [
        'SVG',
    ]

    command = [
        'kabeja',
        '-nogui',
        '-pipeline',
        'svg',
        '$IN',
        '$OUT',
    ]
