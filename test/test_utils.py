"""
Tests for `utils` module.
"""
import pytest

from omnithumb.types import utils

class TestDirectedGraph:
    def setup_method(self, method):
        self.dg = utils.DirectedGraph()

    #  ,-> F,-> E
    # A -> B -> C
    #       '-> D
    def _simple_tree(self):
        self.dg.add_edge('A', 'B', 1)
        self.dg.add_edge('A', 'F', 1)
        self.dg.add_edge('B', 'E', 1)
        self.dg.add_edge('B', 'C', 1)
        self.dg.add_edge('B', 'D', 1)

    def test_simple_routes(self):
        self._simple_tree()
        path = self.dg.shortest_path('A', 'B')
        assert path == ['A', 'B']
        path = self.dg.shortest_path('A', 'C')
        assert path == ['A', 'B', 'C']
        path = self.dg.shortest_path('A', 'E')
        assert path == ['A', 'B', 'E']
        path = self.dg.shortest_path('A', 'D')
        assert path == ['A', 'B', 'D']
        path = self.dg.shortest_path('B', 'C')
        assert path == ['B', 'C']

    def test_raises_on_invalid_path(self):
        with pytest.raises(utils.DirectedGraph.NoPath):
            cost, path = self.dg.shortest_path('B', 'A')

