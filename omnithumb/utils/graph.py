import math
import functools

class DirectedGraph:
    '''
    Simple weighted directed graph implementation with memoized naive algorithm
    for shortest path.
    '''

    class NoPath(ValueError): pass
    def __init__(self):
        self.edges = {}

    def add_edge(self, a, b, cost=1):
        if cost <= 0:
            raise ValueError('DirectedGraph requires positive costs')
        if a == b:
            raise ValueError('DirectedGraph prohibits edges to self')
        self.edges.setdefault(a, {})
        self.edges[a][b] = cost
        self.get_all_paths_from.cache_clear()
        self.get_shortest_paths.cache_clear()

    @functools.lru_cache(maxsize=None)
    def get_all_paths_from(self, start, seen=None):
        '''
        Return a list of all paths to all nodes from a given start node
        '''
        if seen is None:
            seen = frozenset()
        results = [(0, (start, ))]
        if start in seen or start not in self.edges:
            return results
        seen = seen | frozenset((start,))
        for node, edge_weight in self.edges[start].items():
            for subpath_weight, subpath in self.get_all_paths_from(node, seen):
                total_weight = edge_weight + subpath_weight
                full_path = (start, ) + subpath
                results.append((total_weight, full_path))
        return tuple(results)

    @functools.lru_cache(maxsize=None)
    def get_shortest_paths(self):
        '''
        Return a dictionary containing lists of all possible paths within the
        graph, keyed by tuple of start and end
        '''
        shortest_paths = {}
        for start in self.edges:
            paths_from_start = self.get_all_paths_from(start)
            for weight, path in paths_from_start:
                end = path[-1]
                if start == end:
                    continue # Skip over self paths
                shortest, _ = shortest_paths.get((start, end), (math.inf, None))
                if weight < shortest:
                    shortest_paths[(start, end)] = (weight, path)
        return shortest_paths

    def shortest_path(self, start, end):
        '''
        Given a start node and end node, return a tuple containing the shortest
        path from start to end.

        Raise DirectedGraph.NoPath error if no such path exists.
        '''
        shortest_paths = self.get_shortest_paths()
        try:
            return shortest_paths[(start, end)][1] # 1 is path
        except KeyError:
            raise self.NoPath("%s -> %s" % (start, end))
