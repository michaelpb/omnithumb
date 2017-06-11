import pytest
from .testing_utils import E2ETestMixin

class TestContribTest(E2ETestMixin):
    def test_jpeg(self):
        request, response = self.app.test_client.get('/test/test.jpg')
        assert response.status == 200

    def test_png(self):
        request, response = self.app.test_client.get('/test/test.png')
        assert response.status == 200

    def test_zip(self):
        request, response = self.app.test_client.get('/test/empty.zip')
        assert response.status == 200

