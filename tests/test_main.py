import networkx as nx
from main import dijkstra, calculate_toll, create_graph

def test_dijkstra():
    G = create_graph()
    path, cost = dijkstra(G, 'A', 'E')
    assert path == ['A', 'C', 'D', 'E']
    assert cost == 12

    toll = calculate_toll(path, G)
    assert toll == 6

test_dijkstra()
print("All tests passed!")
