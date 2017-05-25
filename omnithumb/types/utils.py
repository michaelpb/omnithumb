class DirectedGraph:
    '''
    Simple weighted directed graph implementation with a memoized shortest path built in.
    '''
    def __init__(self):
        self.edges = {}
        self.edge_payloads = {}
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

