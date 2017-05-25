"""
Tests for `TypeString` module.
"""
import pytest

import tempfile
from base64 import b64decode

from omnithumb.types.typestring import TypeString, guess_typestring

PIXEL_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
PIXEL_B = b64decode(PIXEL_B64)

class TestMimeTypeTypeString:
    @classmethod
    def setup_class(cls):
        cls.ts = TypeString('application/json')

    def test_is_mimetype_method(self):
        assert self.ts.mimetype == 'application/json'
        assert self.ts.extension == 'JSON'
        assert not self.ts.is_qualifier

    def test_str(self):
        assert str(self.ts) == 'application/json'

    def test_has_no_arguments(self):
        assert self.ts.arguments == tuple()

    def test_modify_basename(self):
        assert self.ts.modify_basename('thing.xml') == 'thing.xml.json'
        assert self.ts.modify_basename('thing') == 'thing.json'

class TestExtensionTypeString:
    @classmethod
    def setup_class(cls):
        cls.ts = TypeString('JPEG')

    def test_is_mimetype_method(self):
        assert self.ts.mimetype == 'image/jpeg'
        assert self.ts.extension == 'JPEG'
        assert not self.ts.is_qualifier

    def test_str(self):
        assert str(self.ts) == 'JPEG'

    def test_has_no_arguments(self):
        assert self.ts.arguments == tuple()

    def test_modify_basename(self):
        assert self.ts.modify_basename('thing.xml') == 'thing.xml.jpeg'
        assert self.ts.modify_basename('thing') == 'thing.jpeg'

class TestQualifierArgumentsTypeString:
    @classmethod
    def setup_class(cls):
        cls.ts = TypeString('thumb.png:400x300')

    def test_is_mimetype_method(self):
        assert self.ts.mimetype == None
        assert self.ts.extension == None
        assert self.ts.is_qualifier

    def test_str(self):
        assert str(self.ts) == 'thumb.png:400x300'

    def test_has_arguments(self):
        assert self.ts.arguments == ('400x300',)

    def test_modify_basename(self):
        assert self.ts.modify_basename('thing.xml') == 'thing.xml.400x300.thumb.png'
        assert self.ts.modify_basename('thing') == 'thing.400x300.thumb.png'

class TestGuessPNGTypeString:
    @classmethod
    def setup_class(cls):
        # NOTE: Only works since it has a proper extension
        cls.fd = tempfile.NamedTemporaryFile(suffix='test.png')
        cls.fd.write(PIXEL_B)
        cls.ts = guess_typestring(cls.fd.name)

    def test_guesses_by_extension_correctly(self):
        assert self.ts.mimetype == 'image/png'

    @classmethod
    def teardown_class(cls):
        cls.fd.close()
