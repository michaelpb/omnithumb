import os
import asyncio
import subprocess

from omnithumb.utils.graph import DirectedGraph
from omnithumb.utils.iter import pair_looper
from .typestring import TypeString

class Converter:
    cost = 1
    def __init__(self, config):
        self.config = config


class ExecConverter(Converter):
    def get_arguments(self, resource):
        return resource.typestring.arguments

    def get_command(self, in_resource, out_resource):
        args = self.get_arguments(out_resource)
        replacements = {
            '$IN': in_resource.cache_path,
            '$OUT': out_resource.cache_path,
        }

        # Add in positional arguments ($0, $1, etc)
        for i, arg in enumerate(args):
            replacements['$' + str(i)] = arg

        # Returns list of truthy replaced arguments in command
        return [replacements.get(arg, arg) for arg in self.command]

    # TODO: Fix this, figure out how to test
    #async def convert(self, in_resource, out_resource):
    #    cmd = self.get_command(in_resource, out_resource)
    #    return asyncio.create_process_exec(*cmd)

    def convert_sync(self, in_resource, out_resource):
        cmd = self.get_command(in_resource, out_resource)
        return subprocess.run(cmd)

    convert = convert_sync


class HardLinkConverter(Converter):
    def convert(self, in_resource, out_resource):
        os.link(in_resource.cache_path, out_resource.cache_path)


class ConverterGraph:
    def __init__(self, converter_list):
        self.dgraph = DirectedGraph()
        self.converters = {}
        for converter in converter_list:
            for in_ in converter.inputs:
                for out in converter.outputs:
                    self.dgraph.add_edge(in_, out, converter.cost)
                    self.converters[(in_, out)] = converter

    def find_path(self, in_, out):
        in_f = in_.ts_format
        out_f = out.ts_format
        path = self.dgraph.shortest_path(in_f, out_f)
        results = []
        # Loop through each edge traversal, adding converters and type
        # string pairs as we go along
        for left, right in pair_looper(path):
            converter = self.converters.get((left, right))
            ts_left = TypeString(left)
            ts_right = out if out.ts_format == right else TypeString(right)
            results.append((converter, ts_left, ts_right))
        return results

