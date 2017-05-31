import asyncio
from omnithumb.types.resource import TypedResource, ForeignResource, TypedLocalResource

async def convert(config, uri, to_type, enqueue_method=None, download_method=None):
    if uri.startswith('/'):
        # Absolute path to a file, use local everything
        typed_foreign_res = TypedLocalResource(config, uri)
        resource_class = TypedLocalResource
    else:
        # Need to first download (blocking for now :/)
        foreign_res = ForeignResource(config, uri)
        if foreign_res.exists():
            foreign_res.download()

        resource_class = TypedResource

        # Determine the file type of the foreign resource
        typed_foreign_res = foreign_res.guess_typed()

        if not typed_foreign_res.cache_exists():
            # Symlink to new location that includes typed extension
            typed_foreign_res.symlink_from(foreign_res)

    # Now find path between types
    original_ts = typed_foreign_res.typestring
    path = config.converter_graph.find_path(original_ts, to_type)

    # Loop through each step in graph path and convert
    is_first = True
    for converter_class, from_ts, to_ts in path:
        converter = converter_class(config)
        in_resource = resource_class(config, uri, from_ts)
        if is_first: # Ensure first resource is just the source one
            in_resource = typed_foreign_res
        out_resource = resource_class(config, uri, to_ts)
        if enqueue_method:
            enqueue_method(converter, in_resource, out_resource)
        else:
            await converter.convert(in_resource, out_resource)
        is_first = False

