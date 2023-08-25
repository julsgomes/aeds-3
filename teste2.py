import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def read_data_files(politicians_file, graph_file):
    politicians = {}
    with open(politicians_file, 'r') as file:
        for line in file:
            name, party, _ = line.strip().split(';')
            politicians[name] = party

    graph = {}
    with open(graph_file, 'r') as file:
        for line in file:
            deputado1, deputado2, votes_equal = line.strip().split(';')
            if deputado1 not in graph:
                graph[deputado1] = {}
            graph[deputado1][deputado2] = int(votes_equal)

    return politicians, graph

def filter_parties(graph, politicians, parties_to_filter):
    filtered_graph = {deputado1: {deputado2: votes_equal for deputado2, votes_equal in connections.items()
                                  if politicians[deputado2] not in parties_to_filter}
                      for deputado1, connections in graph.items()
                      if politicians[deputado1] not in parties_to_filter}
    return filtered_graph

def invert_weights(graph):
    inverted_graph = {deputado1: {deputado2: 1 - votes_equal
                                  for deputado2, votes_equal in connections.items()}
                      for deputado1, connections in graph.items()}
    return inverted_graph

def dijkstra(graph, start_node):
    distances = {node: float('inf') for node in graph.keys()}
    predecessors = {node: None for node in graph.keys()}
    distances[start_node] = 0
    unvisited_nodes = list(graph.keys())
    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: distances[node])
        unvisited_nodes.remove(current_node)
        for neighbor, weight in graph[current_node].items():
            new_distance = distances[current_node] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
    return distances, predecessors

def calculate_betweenness_dijkstra(graph):
    betweenness_centrality = {node: 0 for node in graph.keys()}
    for node in graph.keys():
        _, predecessors = dijkstra(graph, node)
        for predecessor in predecessors.values():
            if predecessor:
                betweenness_centrality[predecessor] += 1

    max_betweenness = max(betweenness_centrality.values())
    if max_betweenness > 0:
        betweenness_centrality = {node: value / max_betweenness for node, value in betweenness_centrality.items()}

    return betweenness_centrality

def create_heatmap(matrix, names):
    # Converting the matrix to a DataFrame for visualization
    df = pd.DataFrame(matrix, index=names, columns=names)
    
    # Creating a heatmap using seaborn
    plt.figure(figsize=(15, 15))
    sns.heatmap(df, cmap="YlOrRd", linewidths=.5)
    plt.title("Heatmap of Correlations between Deputados")
    plt.show()

# Example usage:
# create_heatmap(correlation_matrix, deputados_names)

# Generate heatmap
def generate_heatmap(correlation_matrix, nodes_corr):
    # Creating a DataFrame from the correlation matrix
    correlation_df = pd.DataFrame(correlation_matrix, index=nodes_corr, columns=nodes_corr)

    # Defining a custom color palette that ranges from red to yellow (inverted)
    inverted_palette = sns.color_palette("YlOrRd_r", as_cmap=True)

    # Displaying the heatmap with the inverted color palette and the names of the deputados
    plt.figure(figsize=(20, 20))
    sns.heatmap(correlation_df, cmap=inverted_palette, xticklabels=nodes_corr, yticklabels=nodes_corr, linewidths=.5)
    plt.title("Heatmap of Correlation Between Deputados")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.show()

def read_data_files(politicians_file, graph_file):
    politicians = {}
    with open(politicians_file, 'r') as file:
        for line in file:
            name, party, _ = line.strip().split(';')
            politicians[name] = party

    graph = {}
    with open(graph_file, 'r') as file:
        for line in file:
            deputado1, deputado2, votes_equal = line.strip().split(';')
            if deputado1 not in graph:
                graph[deputado1] = {}
            graph[deputado1][deputado2] = int(votes_equal)

    return politicians, graph

def filter_parties(graph, politicians, parties_to_filter):
    filtered_graph = {deputado1: {deputado2: votes_equal for deputado2, votes_equal in connections.items()
                                  if politicians[deputado2] not in parties_to_filter}
                      for deputado1, connections in graph.items()
                      if politicians[deputado1] not in parties_to_filter}
    return filtered_graph

def normalize_weights(graph):
    weights = [votes_equal for connections in graph.values() for votes_equal in connections.values()]
    if not weights:
        return graph
    max_weight = max(weights)
    normalized_graph = {deputado1: {deputado2: votes_equal / max_weight
                                    for deputado2, votes_equal in connections.items()}
                        for deputado1, connections in graph.items()}
    return normalized_graph

def invert_weights(graph):
    inverted_graph = {deputado1: {deputado2: 1 - votes_equal
                                  for deputado2, votes_equal in connections.items()}
                      for deputado1, connections in graph.items()}
    return inverted_graph

def create_correlation_matrix(graph):
    nodes = list(graph.keys())
    matrix = np.zeros((len(nodes), len(nodes)))
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            matrix[i, j] = graph[node1].get(node2, 0.0)
    return matrix, nodes

def plot_heatmap(matrix, labels, cmap='Reds_r'):
    plt.figure(figsize=(10, 10))
    plt.imshow(matrix, cmap=cmap, origin='upper', vmin=0, vmax=1)
    plt.colorbar(label="Correlation")
    plt.xticks(np.arange(len(labels)), labels, rotation=90)
    plt.yticks(np.arange(len(labels)), labels)
    plt.title("Heatmap of Correlation Between Deputies")
    plt.xlabel("Deputies")
    plt.ylabel("Deputies")
    plt.tight_layout()
    plt.show()
