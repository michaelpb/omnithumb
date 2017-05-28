"""
Tests for `responses` module.
"""
import pytest

import tempfile
import os
from base64 import b64decode
from asyncio import iscoroutine, wait

from omnithumb.types.typestring import TypeString, guess_typestring
from omnithumb.responses import placeholder


PIXEL_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='
PIXEL_B = b64decode(PIXEL_B64)
class ExampleBytesPlaceholder(placeholder.BytesPlaceholder):
    types = [
        'PNG',
        'JPG',
    ]
    content_type = 'image/png'
    bytes = PIXEL_B

class ExampleCustomPlaceholder(placeholder.Placeholder):
    types = [
        'JPEG',
        'JPG',
    ]
    content_type = 'image/jpeg'
    JPG_TEST_BYTES = bytes([0xff, 0xd8, 0xff, 0xe0])
    async def stream_response(self, response):
        response.write(self.JPG_TEST_BYTES)

class ExampleWildcardPlaceholder(placeholder.Placeholder):
    types = all
    content_type = 'image/png'
    PNG_TEST_BYTES = bytes([0x89, 0x50, 0x4e, 0x47])
    async def stream_response(self, response):
        response.write(self.PNG_TEST_BYTES)

class MockConfig:
    PLACEHOLDERS = [
        ExampleBytesPlaceholder,
        ExampleCustomPlaceholder,
        ExampleWildcardPlaceholder,
    ]

class TestResponsePlaceholders:
    @classmethod
    def setup_class(cls):
        cls.phs = placeholder.PlaceholderSelector(MockConfig)

    def test_get_placeholder(self):
        ph = self.phs.get_placeholder(TypeString('PNG'))
        assert isinstance(ph, ExampleBytesPlaceholder)
        ph = self.phs.get_placeholder(TypeString('JPEG'))
        assert isinstance(ph, ExampleCustomPlaceholder)
        ph = self.phs.get_placeholder(TypeString('nonexistent'))
        assert isinstance(ph, ExampleWildcardPlaceholder)

        # Temporarily disable
        ExampleWildcardPlaceholder.types = []
        ph = self.phs.get_placeholder(TypeString('nonexistent'))
        assert ph is None
        ExampleWildcardPlaceholder.types = all # restore

    def test_placeholder_stream_response(self):
        class mock_response:
            @staticmethod
            def write(data):
                mock_response.data = data
            @staticmethod
            def stream(streamer=None, content_type=None):
                mock_response.ct = content_type
                # For now, too hard to test this bit
                #coro = streamer(mock_response)
                #assert iscoroutine(coro)
                #yield from coro(mock_response)

        self.phs.stream_response(TypeString('PNG'), mock_response)
        assert mock_response.ct == 'image/png'
        #assert mock_response.data == PIXEL_B

        self.phs.stream_response(TypeString('JPEG'), mock_response)
        assert mock_response.ct == 'image/jpeg'
        #assert mock_response.data == JPG_TEST_BYTES

        self.phs.stream_response(TypeString('lol'), mock_response)
        assert mock_response.ct == 'image/png'
        #assert mock_response.data == PNG_TEST_BYTES

