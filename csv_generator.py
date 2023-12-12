import csv
import random

def generate_graph_csv(graph_type, num_entries):
  # Define file name based on graph type
  file_name = f"{graph_type}_graph.csv"

  # Generate vertices
  vertices = range(1, num_entries)

  # Generate edges and weights (if applicable)
  edges = [(random.choice(vertices), random.choice(vertices))
           for _ in range(num_entries)]

  if 'weighted' in graph_type:
    weights = [random.randint(1, 200) for _ in range(num_entries)]
    edges_with_weights = list(zip(edges, weights, strict=False))
  else:
    edges_with_weights = edges

  with open(file_name, mode='w', newline='') as file:
    if 'weighted' in graph_type:
      writer = csv.writer(file)
      writer.writerow(['source', 'target', 'weight'])
      for edge, weight in edges_with_weights:
        writer.writerow([edge[0], edge[1], weight])
    else:
      writer = csv.writer(file)
      writer.writerow(['source', 'target'])
      for edge in edges:
        writer.writerow([edge[0], edge[1]])
  print(f"Graph CSV file generated: {file_name}")


# Example usage:
# Generate an undirected unweigthed graph with 20 entries
generate_graph_csv('undirected', 20)

#Generate a directed weighted graph with 20 entries
generate_graph_csv('weighted', 20)

