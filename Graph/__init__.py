from .vertex import Vertex
from .graph import Graph
from .directed import Directed
from .undirected import Undirected


# Dijkstra shortest path
def find_shortest_paths(g: Graph, start_vertex: Vertex) -> None:
    """
    Algorithm to find the shortest path from point a to point b in a graph.
    Time Complexity: O(n^2)
    :param g: Graph for which Dijkstra's algorithm is ran against
    :param start_vertex: starting point of graph
    :return: none
    """
    # Put all vertices in an unvisited queue.
    unvisited_queue = []

    for current_vertex in g.adjacency_list:
        current_vertex.reset()
        unvisited_queue.append(current_vertex)

    # Start_vertex has a distance of 0 from itself
    start_vertex.distance = 0

    # One vertex is removed with each iteration; repeat until the list is
    # empty.
    while unvisited_queue:

        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            # print(unvisited_queue[i].label, unvisited_queue[i].distance, unvisited_queue[i].pred_vertex)
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)
        # print("From Start Vetex to current_vertex.label: " + current_vertex.label +" distance: " + str(
        # current_vertex.distance))

        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in g.adjacency_list[current_vertex]:  # values from  dictionary
            # if current_vertex = vertex_1 => adj_vertex in [vertex_2, vertex_3], if vertex_2 => adj_vertex in [
            # vertex_6], ...
            edge_weight = g.edge_weights[(current_vertex, adj_vertex)]  # values from dictionary
            # edge_weight = 484 then 626 then 1306, ...}
            alternative_path_distance = current_vertex.distance + edge_weight

            # If shorter path from start_vertex to adj_vertex is found, update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.previous_vertex = current_vertex
