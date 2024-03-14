import networkx as nx
import matplotlib.pyplot as plt
import timeit
from tabulate import tabulate

def is_independent_set(graph, node_set):
    for node1 in node_set:
        for node2 in graph.neighbors(node1):
            if node2 in node_set:
                return False
    return True

def greedy(graph):
    nodes = list(graph.nodes())
    minimum_maximal_set = set()

    for node in nodes:
        candidate_set = minimum_maximal_set | {node}

        if is_independent_set(graph, candidate_set):
            minimum_maximal_set = candidate_set

    return minimum_maximal_set

def highest_degree(graph):
    remaining_vertices = set(graph.nodes)
    mmis = set()
   
    while remaining_vertices:
        # Find the vertex with the highest degree
        max_degree_vertex = max(remaining_vertices, key=lambda v: graph.degree[v])

        # Add the selected vertex to the minimal maximal set
        mmis.add(max_degree_vertex)

        # Remove the selected vertex and its neighbors from the remaining vertices
        remaining_vertices -= {max_degree_vertex} | set(graph.neighbors(max_degree_vertex))

    return mmis

# Generate a random graph
def generate_connected_random_graph(num_nodes, probability):
    connected = False
    while not connected:
        graph = nx.gnp_random_graph(num_nodes, probability)
        connected = nx.is_connected(graph)
    return graph
probability = 0.2
random_graph = generate_connected_random_graph(20, probability)

# Measure running time for the Greedy algorithm
start_time_Greedy = timeit.default_timer()
min_max_ind_set_Greedy = greedy(random_graph)
end_time_Greedy = timeit.default_timer()
Greedy_time = end_time_Greedy - start_time_Greedy

# Measure running time for the highest degree algorithm
start_time_highest_degree = timeit.default_timer()
min_max_ind_set_highest_degree = highest_degree(random_graph)
end_time_highest_degree = timeit.default_timer()
highest_degree_time = end_time_highest_degree - start_time_highest_degree

# Draw the random graph with the result from the Greedy algorithm
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(random_graph)
nx.draw(random_graph, pos, with_labels=True, node_color='#35ADC8', node_size=500, font_weight='bold', font_color='black')
nx.draw_networkx_nodes(random_graph, pos, nodelist=list(min_max_ind_set_Greedy), node_color='#FC3805', node_size=500, label='Greedy Algorithm')
plt.title("Random Graph and Minimum Maximal Independent Set (Greedy Algorithm)")
plt.legend()
plt.show()

# Draw the same random graph with the result from the highest degree algorithm
plt.figure(figsize=(10, 10))
nx.draw(random_graph, pos, with_labels=True, node_color='#35ADC8', node_size=500, font_weight='bold', font_color='black')
nx.draw_networkx_nodes(random_graph, pos, nodelist=list(min_max_ind_set_highest_degree), node_color='#FCCF07', node_size=500, label='Highest Degree Algorithm')
plt.title("Random Graph and Minimum Maximal Independent Set (Highest Degree Algorithm)")
plt.legend()
plt.show()

# Display the running times in a table
table_data = [
    ["Algorithm", "Running Time"],
    ["Greedy", f"{Greedy_time:.8f} seconds"],
    ["Highest Degree", f"{highest_degree_time:.8f} seconds"]
]

table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
print(table)

# Create a bar graph to visualize running times
algorithms = ["Greedy", "Highest Degree"]
running_times = [Greedy_time, highest_degree_time]

plt.bar(algorithms, running_times, color=['#FC3805', '#FCCF07'])
plt.ylabel('Running Time (seconds)')
plt.title('Algorithm Running Times')
plt.show()

# Create a bar graph to visualize set lengths
lengths = [len(min_max_ind_set_Greedy), len(min_max_ind_set_highest_degree)]
plt.bar(algorithms, lengths, color=['#FC3805', '#FCCF07'])
plt.ylabel('MMIS Length)')
plt.title('Found Set Size')
plt.show()

def run_algorithm_multiple_times(algorithm_func, graph, num_runs=50):
    running_times = []
    length = []

    for _ in range(num_runs):
        start_time = timeit.default_timer()
        result = len(algorithm_func(graph))
        end_time = timeit.default_timer()

        running_times.append(end_time - start_time)
        length.append(result)

    return sum(running_times) / num_runs, sum(length) / num_runs  # Average running time

# Define the number of vertices to test
num_vertices_list = [100, 200, 300, 400, 500]

# Run both algorithms for different numbers of vertices
Greedy_running_times = []
highest_degree_running_times = []
greedy_lengths = []
highest_degree_lengths = []

for num_vertices in num_vertices_list:
    random_graph = generate_connected_random_graph(num_vertices, 0.2)

    Greedy_time, greedy_len = run_algorithm_multiple_times(greedy, random_graph, 50)
    highest_degree_time, highest_degree_len = run_algorithm_multiple_times(highest_degree, random_graph, 50)
    
    greedy_lengths.append(greedy_len)
    highest_degree_lengths.append(highest_degree_len)
    Greedy_running_times.append(Greedy_time)
    highest_degree_running_times.append(highest_degree_time)

# Plotting the results
plt.plot(num_vertices_list, Greedy_running_times, marker='o', label='Greedy Algorithm')
plt.plot(num_vertices_list, highest_degree_running_times, marker='o', label='Highest Degree Algorithm')
plt.xlabel('Number of Vertices')
plt.ylabel('Average Running Time (seconds)')
plt.title('Algorithm Running Time vs. Number of Vertices')
plt.legend()
plt.show()

# Plot lengths
plt.figure(figsize=(10, 6))
plt.plot(num_vertices_list, greedy_lengths, marker='o', label='Greedy Algorithm')
plt.plot(num_vertices_list, highest_degree_lengths, marker='o', label='Highest Degree Algorithm')
plt.xlabel('Number of Vertices')
plt.ylabel('Average Length of Min Max Ind Set')
plt.title('Algorithm Length vs. Number of Vertices')
plt.legend()
plt.show()