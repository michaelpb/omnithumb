import heapq

class MemoizedFunction:
    '''
    Wraps a function and exposes a memoized interface
    '''
    def __init__(self, func):
        self.direct = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        key = (args, tuple(kwargs))
        if key in self.cache:
            return self.cache[key]
        value = self.direct(*args, **kwargs)
        self.cache[key] = value
        return value

    def clear_memoized(self):
        self.cache = {}


def memoize(f):
    """
	Memoization decorator for functions taking one or more arguments.
	"""
    return MemoizedFunction(f)


class DirectedGraph:
    class NoPath(ValueError): pass
    '''
    Simple weighted directed graph implementation with Dijkstra's
    algorithm for shortest path
    '''
    def __init__(self):
        self.edges = {}

    def add_edge(self, a, b, cost=1):
        self.edges.setdefault(a, {})
        self.edges[a][b] = cost

    def find_path(self, start, end):
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
                if vertex not in graph:
                    raise DirectedGraph.NoPath()
                for (next, c) in graph[vertex].items():
                    heapq.heappush(queue, (cost + c, next, path))

        return result



START = object() # just using as a unique symbol
def pair_looper(iterator):
    left = START
    for item in iterator:
        if left is not START:
            yield (left, item)
        left = item
