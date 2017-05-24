import hashlib
import os
import requests
import shutil
import asyncio
from itertools import zip_longest
from urllib.parse import urlparse

def group_by(iterable, n, fill=None):
    args = [iter(iterable)] * n
    return list(''.join(s) for s in zip_longest(*args, fillvalue=fill))

def check_url(config, url):
    if url.netloc not in config.ALLOWED_LOCATIONS:
        pass # TODO add security checking here

class DEFAULT_CONFIG:
    PATH_PREFIX = '/tmp/omnithumb/'
    ALLOWED_LOCATIONS = {'localhost:8080'}
    PATH_GROUPING = 'MD5'

class URLError(ValueError): pass

class Resource:
    '''
    Provide a high-level Resource object that based on a config and a
    URL, and a prefix representing what type of resource this will be
    '''
    def __init__(self, config, url, prefix='orig'):
        if not config:
            config = DEFAULT_CONFIG
        # Setup props
        self.url_string = url
        self.config = config
        self.prefix = prefix

        # Parse and process URL
        self.url = urlparse(url)
        self.url_path_split = self.url.path.split('/')
        self.url_path_basename = self.url_path_split[-1]
        if len(self.url_path_basename) < 1:
            # Path is too small, probably ends with /, try 1 up
            self.url_path_basename = self.url_path_split[-2]
        self.basename = '%s.%s' % (prefix, self.url_path_basename)

        # Generate MD5
        self.md5 = hashlib.md5(self.url_string.encode('utf-8')).hexdigest()

        # Generate filepath
        self.cache_path = os.path.join(
                self.config.PATH_PREFIX,
                *self.path_grouping(),
                self.basename,
            )

    def path_grouping(self):
        if self.config.PATH_GROUPING == 'MD5':
            return group_by(self.md5, 8)
        return ['']

    def validate(self):
        if not check_url(self.config, self.url):
            raise URLError('Invalid URL: "%s"' % url)

    def __str__(self):
        return self.cache_path

    def cache_exists(self):
        return os.path.exists(self.cache_path)

    def request_get(self):
        return requests.get(self.url_string, stream=True)

    def open_cache(self, mode='wb'):
        dirname = os.path.dirname(self.cache_path)
        os.makedirs(dirname, exist_ok=True)
        return open(self.cache_path, mode)

    async def download(self):
        req = self.request_get()
        with self.open_cache() as f:
            shutil.copyfileobj(req.raw, f)

