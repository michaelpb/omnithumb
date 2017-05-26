"""
Tests for `utils` module.
"""
import pytest

from omnithumb.types import utils

class TestDirectedGraph:
    #  ,-> F ,-> E
    # A -> B  -> C
    #        '-> D
    def _simple_tree(self):
        self.dg = utils.DirectedGraph()
        self.dg.add_edge('A', 'B', 1)
        self.dg.add_edge('A', 'F', 1)
        self.dg.add_edge('B', 'E', 1)
        self.dg.add_edge('B', 'C', 1)
        self.dg.add_edge('B', 'D', 1)

    #  ,-> F - - - -.
    # '    v         v
    # A -> B -> G -> C
    def _multi_pathed_graph(self):
        self.dg = utils.DirectedGraph()
        self.dg.add_edge('A', 'B', 1)
        self.dg.add_edge('B', 'G', 1)
        self.dg.add_edge('G', 'C', 1)
        self.dg.add_edge('A', 'F', 1)
        self.dg.add_edge('F', 'C', 1)
        self.dg.add_edge('F', 'B', 1)

    #  5-> F - - - -.
    # '    v         v
    # A -> B -> G -> C
    def _multi_pathed_graph_weighted(self):
        self.dg = utils.DirectedGraph()
        self.dg.add_edge('A', 'B', 1)
        self.dg.add_edge('B', 'G', 1)
        self.dg.add_edge('G', 'C', 1)
        self.dg.add_edge('A', 'F', 5)
        self.dg.add_edge('F', 'C', 1)
        self.dg.add_edge('F', 'B', 1)

    #  STL  .   MOV .   GIF .
    #  OBJ   -> AVI  -> JPG  -> thumb.png
    #  MESH '   MP4 '   PNG '
    #      \\\         .^
    #       ''---------
    #  MP3 .
    #  WAV  -> cleaned.ogg
    #  OGG '


    def _realistic_edges(self):
        self.dg = utils.DirectedGraph()
        self.dg.add_edge('MOV', 'JPG')
        self.dg.add_edge('AVI', 'JPG')
        self.dg.add_edge('MP4', 'JPG')
        self.dg.add_edge('JPG', 'thumb.png')
        self.dg.add_edge('PNG', 'thumb.png')
        self.dg.add_edge('GIF', 'thumb.png')
        self.dg.add_edge('STL', 'AVI')
        self.dg.add_edge('OBJ', 'AVI')
        self.dg.add_edge('MESH', 'AVI')
        self.dg.add_edge('STL', 'PNG')
        self.dg.add_edge('OBJ', 'PNG')
        self.dg.add_edge('MESH', 'PNG')
        self.dg.add_edge('MP3', 'cleaned.ogg')
        self.dg.add_edge('WAV', 'cleaned.ogg')
        self.dg.add_edge('OGG', 'cleaned.ogg')

    def test_simple_routes(self):
        self._simple_tree()
        path = self.dg.shortest_path('A', 'B')
        assert path == ('A', 'B')
        path = self.dg.shortest_path('A', 'C')
        assert path == ('A', 'B', 'C')
        path = self.dg.shortest_path('A', 'E')
        assert path == ('A', 'B', 'E')
        path = self.dg.shortest_path('A', 'D')
        assert path == ('A', 'B', 'D')
        path = self.dg.shortest_path('B', 'C')
        assert path == ('B', 'C')

    def test_raises_on_invalid_path(self):
        self._simple_tree()
        with pytest.raises(utils.DirectedGraph.NoPath):
            path = self.dg.shortest_path('B', 'A')

    def test_shortest_route(self):
        self._multi_pathed_graph()
        path = self.dg.shortest_path('A', 'B')
        assert path == ('A', 'B')
        path = self.dg.shortest_path('F', 'B')
        assert path == ('F', 'B')
        path = self.dg.shortest_path('F', 'G')
        assert path == ('F', 'B', 'G')
        path = self.dg.shortest_path('F', 'C')
        assert path == ('F', 'C')
        path = self.dg.shortest_path('A', 'G')
        assert path == ('A', 'B', 'G')
        path = self.dg.shortest_path('A', 'C')
        assert path == ('A', 'F', 'C')

    def test_weighted_shortest_route(self):
        self._multi_pathed_graph_weighted()
        path = self.dg.shortest_path('A', 'B')
        assert path == ('A', 'B')
        path = self.dg.shortest_path('F', 'B')
        assert path == ('F', 'B')
        path = self.dg.shortest_path('F', 'G')
        assert path == ('F', 'B', 'G')
        path = self.dg.shortest_path('F', 'C')
        assert path == ('F', 'C')
        path = self.dg.shortest_path('A', 'G')
        assert path == ('A', 'B', 'G')
        path = self.dg.shortest_path('A', 'C')
        assert path == ('A', 'B', 'G', 'C') # Avoid A->F route

    def test_realistic_routing(self):
        self._realistic_edges()
        path = self.dg.shortest_path('STL', 'thumb.png')
        assert path == ('STL', 'PNG', 'thumb.png')
        path = self.dg.shortest_path('MESH', 'JPG')
        assert path == ('MESH', 'AVI', 'JPG')
        path = self.dg.shortest_path('MP3', 'cleaned.ogg')
        assert path == ('MP3', 'cleaned.ogg')
        with pytest.raises(utils.DirectedGraph.NoPath):
            self.dg.shortest_path('MP3', 'thumb.png')

