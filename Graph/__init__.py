from .Vertex import Vertex
from .Directed import Directed as DirectedGraph
from .Undirected import Undirected as UndirectedGraph


def dijkstra_shortest_path(graph, start):
    # Put all vertices in an unvisited queue.
    unvisited_queue = []

    for current_vertex in graph.adjacency_list:
        current_vertex.reset()
        unvisited_queue.append(current_vertex)

    # start has a distance of 0 from itself
    start.distance = 0

    # One vertex is removed with each iteration; reapeat until the list is empty
    while unvisited_queue:

        # Visit vertex with minimum distance from start
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)

        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in graph.adjacency_list[current_vertex]:
            # if current_vertex = vertex_1 => adj_vertex in [vertex_2, vertex_3],
            # if vertex_2 => adj_vertex in [vertex_6], ...
            edge_weight = graph.edge_weights[(current_vertex, adj_vertex)]
            # values from dictionary
            # edge_weight = 484 then 626 then 1306, ...}
            alternative_path_distance = current_vertex.distance + edge_weight
            # If shorter path from start_vertex to adj_vertex is found,
            # update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.previous_vertex = current_vertex