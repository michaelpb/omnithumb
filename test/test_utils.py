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
        cost, path = self.dg.find_path('A', 'B')
        assert cost == 1
        assert path == ['A', 'B']
        cost, path = self.dg.find_path('A', 'C')
        assert cost == 2
        assert path == ['A', 'B', 'C']
        cost, path = self.dg.find_path('A', 'E')
        assert cost == 2
        assert path == ['A', 'B', 'E']
        cost, path = self.dg.find_path('A', 'D')
        assert cost == 2
        assert path == ['A', 'B', 'D']
        cost, path = self.dg.find_path('B', 'C')
        assert cost == 1
        assert path == ['B', 'C']

    def test_raises_on_invalid_path(self):
        with pytest.raises(utils.DirectedGraph.NoPath):
            cost, path = self.dg.find_path('B', 'A')

