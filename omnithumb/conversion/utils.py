import asyncio
from omnithumb.types.resource import TypedResource, ForeignResource, TypedLocalResource, TypedPathedLocalResource
from omnithumb.utils.iter import first_last_iterator

async def convert(config, uri, to_type, enqueue_method=None, download_method=None):
    final_resource_class = None
    if uri.startswith('/'):
        # Absolute path to a file, use local everything
        typed_foreign_res = TypedLocalResource(config, uri)
        resource_class = TypedLocalResource
        final_resource_class = TypedPathedLocalResource
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
    conversion_path = config.converter_graph.find_path(original_ts, to_type)

    # Loop through each step in graph path and convert
    for is_first, is_last, path_step in first_last_iterator(conversion_path):
        converter_class, from_ts, to_ts = path_step
        converter = converter_class(config)
        in_resource = resource_class(config, uri, from_ts)
        if is_first: # Ensure first resource is just the source one
            in_resource = typed_foreign_res
        out_resource = resource_class(config, uri, to_ts)

        if is_last and final_resource_class:
            out_resource = final_resource_class(config, uri, to_ts)

        if enqueue_method:
            enqueue_method(converter, in_resource, out_resource)
        else:
            await converter.convert(in_resource, out_resource)

