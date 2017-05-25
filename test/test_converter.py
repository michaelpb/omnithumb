"""
Tests for `resource` module.
"""
import pytest

import tempfile
import os
from base64 import b64decode

from omnithumb.types.typestring import TypeString
from omnithumb.types.resource import TypedResource
from omnithumb.types import converter

URL = 'http://mocksite.local/file.png'
JPG_TEST_BYTES = bytes([0xff, 0xd8, 0xff, 0xe0])

# TODO: Fix these tests to be less integrate-y, mock out subprocess
# calls

class MockConfig:
    PATH_GROUPING = 'MD5'
    PATH_PREFIX = ''
    ALLOWED_LOCATIONS = '*'

class HardLinkConverter(converter.HardLinkConverter):
    inputs = ['JPEG']
    outputs = ['JPG']

class ExecConverter(converter.ExecConverter):
    inputs = ['JPEG']
    outputs = ['JPG']
    command = [
        'mv',
        '$IN',
        '$OUT',
    ]


class ExecConverterWithArgs(ExecConverter):
    command = [
        'cp',
        '$0',
        '$IN',
        '$OUT',
    ]



class ConverterTestBase:
    def setup_method(self, method):
        self.config = MockConfig
        self.config.PATH_PREFIX = tempfile.mkdtemp()
        self.res = TypedResource(self.config, URL, TypeString('JPEG'))
        self.res2 = TypedResource(self.config, URL, TypeString('JPG'))
        with self.res.cache_open('wb') as f:
            f.write(JPG_TEST_BYTES)

    def teardown_method(self, method):
        try: os.remove(self.res.cache_path)
        except OSError: pass
        if self.res2:
            try: os.remove(self.res2.cache_path)
            except OSError: pass
        try:
            os.removedirs(os.path.dirname(self.res.cache_path))
        except OSError: pass
        try:
            os.removedirs(os.path.dirname(self.res2.cache_path))
        except OSError: pass

    def _check_convert(self):
        self.converter.convert(self.res, self.res2)
        assert self.res2.cache_exists()
        with self.res2.cache_open() as f:
            assert f.read() == JPG_TEST_BYTES


class TestHardLinkConverter(ConverterTestBase):
    def test_convert(self):
        self.converter = HardLinkConverter(self.config)
        self._check_convert()


class TestExecConverter(ConverterTestBase):
    def test_convert(self):
        self.converter = ExecConverter(self.config)
        self._check_convert()

    def test_convert_with_arg(self):
        # cp -s creates a symbolic link
        self.res2 = TypedResource(self.config, URL, TypeString('JPG:-s'))
        self.converter = ExecConverterWithArgs(self.config)
        self._check_convert()
        assert os.path.islink(self.res2.cache_path)


class TestBasicConverterGraph(ConverterTestBase):
    def test_properties(self):
        self.converter_graph = converter.ConverterGraph(self.config)

