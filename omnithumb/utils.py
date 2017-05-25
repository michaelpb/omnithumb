import hashlib
import os
import shutil
import asyncio
import heapq
from itertools import zip_longest
from urllib.parse import urlparse

import requests

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

    def open_cache(self, mode='rb'):
        if mode == 'wb':
            dirname = os.path.dirname(self.cache_path)
            os.makedirs(dirname, exist_ok=True)
        return open(self.cache_path, mode=mode)

    def download(self):
        req = requests.get(self.url_string, stream=True)
        with self.open_cache('wb') as f:
            shutil.copyfileobj(req.raw, f)

    def get_cache_mimetype(self):
        # LOGIC: for 'orig' type files, once
        with self.open_cache() as f:
            mimetype = magic.from_buffer(f.read(128), mime=True)
        return mimetype

    def get_known_ext(self):
        # LOGIC: for 'orig' type files, first try mimetype, then ext
        if self.prefix == 'orig':
            # Validate mimetype against extension
            mimetype = self.get_cache_mimetype()
            if not mimetype:
                # Could not get mimetype from data, just use extension
                return os.path.splitext(self.basename)[1]

            # Can determine mimetype from data, go with that
            return mimetypes.guess_ext(mimetype)

            # TODO
            # More possibly uselsees logic here:
            guessed_mimetype, encoding = mimetypes.guess_type(self.basename)
            if not guessed_mimetype or guessed_mimetype != mimetype:
                # Should log warning, and used current mimetype
                return mimetypes.guess_ext(mimetype)
            return os.path.splitext(self.basename)[1]

        return os.path.splitext(self.basename)[1]

class DirectedGraph:
    '''
    Simple weighted directed graph implementation with a memoized shortest path built in.
    '''
    def __init__(self):
        self.edges = {}
        self._memoized_paths = {}

    def add_edge(self, a, b, cost=1):
        self.edges.setdefault(a, {})
        self.edges[a][b] = cost

    def find_path(self, start, end):
        memoized_key = (start, end)
        if memoized_key in self._memoized_paths:
            return self._memoized_paths[memoized_key]

        # From Chris Laffa's implementation of Dijkstra's algorithm with heapq:
        # http://code.activestate.com/recipes/119466-dijkstras-algorithm-for-shortest-paths/
        queue = [(0, start, [])]
        seen = set()
        graph = self.edges
        result = None
        while True:
            (cost, vertex, path) = heapq.heappop(queue)
            if vertex not in seen:
                path = path + [vertex]
                seen.add(vertex)
                if vertex == end:
                    result = (cost, path)
                    break
                for (next, c) in graph[vertex].items():
                    heapq.heappush(queue, (cost + c, next, path))

        self._memoized_paths[memoized_key] = result
        return result


class Type:
    def __init__(self, mimetype):
        self.mimetype = mimetype

    def check_url(self, resource):
        url = resource.url_string
        request = urllib.request.Request(url)
        response = urlopen(request)
        mimetype = magic.from_buffer(response.read(128), mime=True)
        return self.mimetype == mimetype



