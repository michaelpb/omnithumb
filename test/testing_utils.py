import socketserver
import subprocess
from http.server import BaseHTTPRequestHandler
from multiprocessing import Process

from omnithumb.worker import Worker

def server_process(path, data, mimetype, port=9123):
    class Handler(BaseHTTPRequestHandler):
        def _set_headers(self):
            assert self.path == path
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(data)

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()


def make_server(path, data, mimetype, port=9123):
    class Handler(BaseHTTPRequestHandler):
        def _set_headers(self):
            assert self.path == path
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(data)

    return socketserver.TCPServer(("", port), Handler)

JPG_TEST_BYTES = bytes([0xff, 0xd8, 0xff, 0xe0])

class RunOnceWorker(Worker):
    # XXX Presently unused
    '''
    Worker that just goes through a given queue
    '''
    def __init__(self, queue):
        self.queue = queue

    @property
    def running(self):
        return bool(self.queue)

    async def get_next(self):
        return self.queue.pop(0)

    async def check_download(self, foreign_resource):
        self.check_download_was_called = True
        return True

    async def check_convert(self, converter, in_r, out_r):
        self.check_convert_was_called = True
        return True

class E2ETestMixin:
    @classmethod
    def setup_class(cls):
        from omnithumb.config import settings
        from omnithumb.server import runserver
        cls.app = runserver(settings, '127.0.0.1', 123456, just_setup_app=True)

