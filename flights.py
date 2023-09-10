from collections import defaultdict

# List of Airport Codes
airport_codes = ["JFK", "LAX", "ORD", "MIA", "YYZ", "LHR", "CDG", "SYD", "HND", "AMS"]

# List of Connections
connections = [
    ["JFK", "LAX"],  # JFK to LAX
    ["JFK", "ORD"],  # JFK to ORD
    ["JFK", "MIA"],  # JFK to MIA
    ["JFK", "YYZ"],  # JFK to YYZ
    ["JFK", "LHR"],  # JFK to LHR
    ["LAX", "SYD"],  # LAX to SYD
    ["LAX", "HND"],  # LAX to HND
    ["LAX", "CDG"],  # LAX to CDG
    ["ORD", "AMS"],  # ORD to AMS
    ["ORD", "LHR"],  # ORD to LHR
    ["MIA", "CDG"],  # MIA to CDG
    ["MIA", "LHR"],  # MIA to LHR
    ["MIA", "HND"],  # MIA to HND
    ["YYZ", "AMS"],  # YYZ to AMS
    ["YYZ", "CDG"],  # YYZ to CDG
    ["LHR", "CDG"],  # LHR to CDG
    ["LHR", "SYD"],  # LHR to SYD
    ["CDG", "AMS"],  # CDG to AMS
    ["SYD", "HND"],  # SYD to HND
    ["HND", "AMS"],  # HND to AMS
    ["AMS", "CDG"],  # AMS to CDG
]

# Starting Airport
starting_airport = "JFK"

# Create the adjacency list
adjacency_list = defaultdict(list)


# dfs The algorithm is based on deep first search
def dfs(graph, d, visited_vertex, component):
    visited_vertex[d] = True
    component.append(d)
    for i in graph[d]:
        if not visited_vertex[i]:
            dfs(graph, i, visited_vertex, component)


# fill the stack
def fill_order(graph, d, visited_vertex, stack):
    visited_vertex[d] = True
    for i in graph[d]:
        if not visited_vertex[i]:
            fill_order(graph, i, visited_vertex, stack)
    stack.append(d)


# transpose the matrix (kosaraju) this is reverse the graph
def transpose(graph):
    g = defaultdict(list)

    for i in graph:
        for j in graph[i]:
            g[j].append(i)
    return g


# Find strongly connected components
def get_scc(graph, V):
    stack = []
    visited_vertex = [False] * V
    components = []

    for i in range(V):
        if not visited_vertex[i]:
            fill_order(graph, i, visited_vertex, stack)

    gr = transpose(graph)

    visited_vertex = [False] * V

    while stack:
        i = stack.pop()
        if not visited_vertex[i]:
            component = []
            dfs(gr, i, visited_vertex, component)
            components.append(component)

    return components


# Find the number of new connections
def number_of_new_connections(starting_airport, airport_codes, connections):
    # Process de input
    airports_processed = defaultdict(list)
    for i in range(len(airport_codes)):
        airports_processed[airport_codes[i]] = i

    # Create the adjacency list
    for connection in connections:
        start_airport, end_airport = connection
        start_index = airport_codes.index(start_airport)
        end_index = airport_codes.index(end_airport)

        adjacency_list[start_index].append(end_index)

    # Get the strongly connected components
    scc = get_scc(adjacency_list, len(airport_codes))

    # Create compressed SCCs list
    compressed_scc = []
    # Iterate through the SCCs list
    for sublist in scc:
        # Check if the sublist has more than one element
        if len(sublist) > 1:
            # If it does, add only the first item from the sublist
            compressed_scc.append([sublist[0]])
        else:
            # If it has only one element, add it as is
            compressed_scc.append(sublist)

    # Degrees map for each node in the graph
    degrees = {}
    count = 0
    not_added = []

    # Loop through the adjacency list to see which components will have indegree 1, this is that
    # at least one connection is done inbound them
    for airport in adjacency_list.keys():
        for component in scc:
            if len(component) == 1:
                for node in adjacency_list[airport]:
                    if component[0] == node and component[0] != airports_processed[starting_airport]:
                        degrees[node] = 1
            else:
                for node in adjacency_list[airport]:
                    for item in component:
                        if item == node and item != airports_processed[starting_airport]:
                            degrees[node] = 1

    # Looping through the degree map to see which item was not added, that item will have indegree of 0
    # and if that happens then one new connection needs to be done
    for i in range(len(airport_codes)):
        if i not in degrees.keys() and i != airports_processed[starting_airport]:
            not_added.append(airport_codes[i])
            count += 1

    return {
        "start_airport": starting_airport,
        "connection_count": count,
        "connections": not_added
    }