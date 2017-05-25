import os
import asyncio
import subprocess

from .utils import DirectedGraph

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
        print(cmd)
        return subprocess.run(cmd)

    convert = convert_sync


class HardLinkConverter(Converter):
    def convert(self, in_resource, out_resource):
        os.link(in_resource.cache_path, out_resource.cache_path)


class ConverterGraph:
    def __init__(self, converter_list):
        self.dgraph = DirectedGraph
        self.converters = []
        for converter in self.converter_list:
            for in_ in converter.inputs:
                for out in converter.outputs:
                    self.dgraph.add_edge(in_, out)
                    self.converters[(in_, out)] = converter

    def find_path(self, in_, out):
        total_cost, path = self.dgraph.find_path(str(in_), str(out))
        left = str(in_)
        results = []
        for step in path:
            right = step
            converter = self.converters.get((left, right))
            results.append((converter, TypeString(left), TypeString(right))
        return results

