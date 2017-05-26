import collections
import math

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


START = object() # just using as a unique symbol
def pair_looper(iterator):
    '''
    Loop through iterator yielding items in adjacent pairs
    '''
    left = START
    for item in iterator:
        if left is not START:
            yield (left, item)
        left = item

class DirectedGraph:
    class NoPath(ValueError): pass
    '''
    Simple weighted directed graph implementation with Dijkstra's
    algorithm for shortest path
    '''
    # Inspired by Alex H Wood's blog post: http://alexhwoods.com/dijkstra/
    # Which in turn was inspired by this gist: https://gist.github.com/econchick/4666413
    def __init__(self):
        self.vertices = set()

        # makes the default value for all vertices an empty list
        self.edges = collections.defaultdict(list)
        self.weights = {}

    def add_vertex(self, value):
        self.vertices.add(value)

    def add_edge(self, from_vertex, to_vertex, distance=1):
        if from_vertex == to_vertex:
            pass  # no self-cycles allowed
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        self.edges[from_vertex].append(to_vertex)
        self.weights[(from_vertex, to_vertex)] = distance

    def dijkstra(self, start):
        # initializations
        S = set()

        # delta represents the length shortest distance paths from start -> v, for v in delta. 
        # We initialize it so that every vertex has a path of infinity
        delta = dict.fromkeys(list(self.vertices), math.inf)
        previous = dict.fromkeys(list(self.vertices), None)

        # then we set the path length of the start vertex to 0
        delta[start] = 0

        # while there exists a vertex v not in S
        while S != self.vertices:
            # let v be the closest vertex that has not been visited...it will begin at 'start'
            v = min((set(delta.keys()) - S), key=delta.get)

            # for each neighbor of v not in S
            for neighbor in set(self.edges[v]) - S:
                new_path = delta[v] + self.weights[v, neighbor]

            # is the new path from neighbor through 
            if new_path < delta[neighbor]:
                # since it's optimal, update the shortest path for neighbor
                delta[neighbor] = new_path

                # set the previous vertex of neighbor to v
                previous[neighbor] = v
            S.add(v)
        print('this is deltas', delta)
        print('this is previouses', previous)
        return delta, previous

    def shortest_path(self, start, end):
        if (start, end) in self.weights:
            return [start, end]
        delta, previous = self.dijkstra(start)
        path = []
        vertex = end

        while vertex is not None:
            path.append(vertex)
            if vertex not in previous:
                raise DirectedGraph.NoPath("%s -> %s" % (start, end))
            vertex = previous[vertex]

        path.reverse()
        return path


