# 6.0002 Problem Set 2
# Graph Optimization
# Name: Sandra Tang
# Collaborators: Office Hour Lab Assistants
# Time: 9 hours

#
# Finding shortest paths to drive from home to work on a road network
#


import unittest
from graph import DirectedRoad, Node, RoadMap


# PROBLEM 2: Building the Road Network
#
# PROBLEM 2a: Designing your Graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the times
# represented?
#
# ANSWER: 
# The graph's nodes represent endpoints of a road. 
# The graph's edges represent roads. 
# The times represent time taken to traverse the road.
# They are represented via edge weights.


# PROBLEM 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a road map (graph).

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following format, separated by tabs:
            From To TotalTime  RoadType
        e.g.
            N0	N1	15	interstate
        This entry would become an edge from 'N0' to 'N1' on an interstate highway with 
        a weight of 15. There should also be another edge from 'N1' to 'N0' on an interstate
        using the same weight.

    Returns:
        a directed road map representing the inputted map
    """

    #open the file and load info into a list
    info = []
    with open(map_filename) as f:
        info = f.read().splitlines()

    for i in range(0, len(info)):
        info[i] = info[i].split()

    #add roads to a list of roads
    #add them in both directions
    dir_roads = []
    for i in info:
        dir_roads.append(DirectedRoad(Node(i[0]), Node(i[1]), int(i[2]), i[3]))
        dir_roads.append(DirectedRoad(Node(i[1]), Node(i[0]), int(i[2]), i[3]))
        #print(DirectedRoad(Node(i[0]), Node(i[1]), int(i[2]), i[3]))
    r_map = RoadMap()

    #add node if not already in set nodes
    for i in info:
        if not Node(i[0]) in r_map.get_all_nodes():
            r_map.add_node(Node(i[0]))
        if not Node(i[1]) in r_map.get_all_nodes():
            r_map.add_node(Node(i[1]))
    #add roads to road map
    for i in dir_roads:
        #print("i: ", i)
        r_map.add_road(i)
    return r_map
    

# PROBLEM 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out

# print(load_map("test_load_map.txt"))
# print(load_map("./maps/road_map.txt"))

# PROBLEM 3: Finding the Shortest Path using Optimized Search Method
#
# PROBLEM 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# ANSWER:
# The objective function is to find the path with the shortest travel time. 
# The constraints are:
# start at the start and end at the goal destination
# follow a valid path
# travel time is minimized

# PROBLEM 3b: Implement get_neighbors
def get_neighbors(roadmap, node, restricted_roads):
    """
    Finds the neighbors of a node in a given roadmap, without
    considering roads of type in restricted_roads.

    
    Parameter:
        roadmap: RoadMap
            The graph on which to carry out the search
        node: Node
            node whose neighbors to retrieve
        restricted_roads: list[strings]
            Road Types not under consideration

    Returns:
        list of neighbor nodes
    """
    #get_roads_for_nodes returns
    #a copy of the list of all of the roads for given node

    #get all roads from a node
    roads_for_nodes = roadmap.get_roads_for_node(node)

    #if the node's type is in restricted_roads, don't consider it
    #consider if not in restricted_roads
    #if the road is not restricted, add the destination to a list of neighbors

    neighbors = []
    for r in roads_for_nodes:
        if r.get_type() not in restricted_roads:
            neighbors.append(r.get_destination())
    return neighbors

# PROBLEM 3c: Implement get_best_path
def get_best_path(roadmap, start, end, restricted_roads, to_neighbor = False):
    """
    Finds the shortest path between nodes subject to constraints.

    Parameters:
        roadmap: RoadMap
            The graph on which to carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
        restricted_roads: list[strings]
            Road Types not allowed on path
        to_neighbor: boolean
            flag to indicate whether to get shortest path to end or
            shortest path to some neighbor of end 

    Returns:
        A tuple of the form (best_path, best_time).
        The first item is the shortest-path from start to end, represented by
        a list of nodes (Nodes).
        The second item is an integer, the length (time traveled)
        of the best path.

        If there exists no path that satisfies restricted_roads constraints, then return None.
    """

    
    # Write Dijkstra implementation here

    # PROBLEM 4c: Handle the to_neighbor = True case here

    #def get_best_path(roadmap, start, end, restricted_roads, to_neighbor = False):

    #if either start or end is not a valid node, return None
    if not roadmap.has_node(start) or not roadmap.has_node(end):
        return None
    #if start and end are the same node, return ([], 0) # Empty path with 0 travel time
    if start == end:
        return ([], 0)

    #Label every node as unvisited
    unvisited = roadmap.get_all_nodes()
    distanceTo = {node: float('inf') for node in roadmap.get_all_nodes()}
    distanceTo[start] = 0
    # Mark all nodes as not having found a predecessor node on path
    #from start
    predecessor = {node: None for node in roadmap.get_all_nodes()}

    while unvisited:
        # Select the unvisited node with the smallest distance from 
        # start, it's current node now.
        current = min(unvisited, key=lambda node: distanceTo[node])

        # Stop, if the smallest distance 
        # among the unvisited nodes is infinity.
        if distanceTo[current] == float('inf'):
            break

        # Find unvisited neighbors for the current node 
        # and calculate their distances from start through the
        # current node.

        #iterate thru roads starting from current node
        for neighbour_road in roadmap.get_roads_for_node(current):

            #add road's time to total time
            alternativePathDist = distanceTo[current] + neighbour_road.get_total_time() #hops as distance

            # Compare the newly calculated distance to the assigned. 
            # Save the smaller distance and update predecssor.
            if alternativePathDist < distanceTo[neighbour_road.get_destination()]:
                if neighbour_road.get_type() in restricted_roads:
                    distanceTo[neighbour_road.get_destination()] = float('inf')
                else:
                    distanceTo[neighbour_road.get_destination()] = alternativePathDist
                predecessor[neighbour_road.get_destination()] = current

        # Remove the current node from the unvisited set.
        unvisited.remove(current)
            
    #Attempt to be build a path working backwards from end
    path = []
    current = end
    while predecessor[current] != None:
        path.insert(0, current)
        current = predecessor[current]
    if path != []:
        path.insert(0, current)
    else:
        return None

    best_time = distanceTo[end]
    #get the road between two nodes and add the time of that
    #no method explicitly for that
    #but there is get_roads_for_node

    #return a tuple
    return (path, best_time)


# PROBLEM 4a: Implement best_path_ideal_traffic
def best_path_ideal_traffic(filename, start, end):
    """Finds the shortest path from start to end during ideal traffic conditions.

    You must use get_best_path and load_map.

    Parameters:
        filename: name of the map file that contains the graph on which
            carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
    Returns:
        The shortest path from start to end in normal traffic,
            represented by a list of nodes (Nodes).

        If there exists no path, then return None.
    """
    graph = load_map(filename)
    #load_map returns a road map object

    #get_best_path returns (best path, best time)
    #run method and get the best path
    best_path = get_best_path(graph, start, end, None)[0]

    if best_path == None:
        return None

    #make list of nodes on that path
    best_nodes = []
    for nodes in best_path:
        best_nodes.append(nodes)
    return best_nodes


# PROBLEM 4b: Implement best_path_restricted
def best_path_restricted(filename, start, end):
    """Finds the shortest path from start to end when local roads cannot be used.

    You must use get_best_path and load_map.

    Parameters:
        filename: name of the map file that contains the graph on which
            carry out the search
        start: Node
            node at which to start
        end: Node
            node at which to end
    Returns:
        The shortest path from start to end given the aforementioned conditions,
            represented by a list of nodes (Nodes).

        If there exists no path that satisfies restricted_roads constraints, then return None.
    """
    graph = load_map(filename)
    #load_map returns a road map object

    #get_best_path returns (best path, best time)
    #run method and get the best path
    #local roads are restricted
    best_path = get_best_path(graph, start, end, ["local"])[0]

    if best_path == None:
        return None

    #make list of nodes on that path
    best_nodes = []
    for nodes in best_path:
        best_nodes.append(nodes)
    return best_nodes

# PROBLEM 4c: Implement best_path_to_neighbor_restricted


# UNCOMMENT THE FOLLOWING LINES TO DEBUG

# rmap = load_map('maps/road_map.txt')

# start = Node('N0')
# end = Node('N1')
# restricted_roads = ['']

# print(get_best_path(rmap, start, end, restricted_roads))
