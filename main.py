import csv
import sys
import os
import copy
import heapq
from collections import deque

class Node:
  def __init__(self, key):
    # Initialize a node with a key and default attributes
    self.key = key
    self.color = "white" # Default color
    self.d = float("inf") # Default distance
    self.pi = None # Default predecessor
    self.neighbors = [] # Adjacency list
    # for DFS
    self.td = 0 # Discovery time
    self.ft = 0 # Finishing time
  
  def __copy__(self):
    # Create a copy of the node
    new_node = self.__class__(self.key)
    new_node.color = self.color
    new_node.d = self.d
    new_node.pi = self.pi
    new_node.td = self.td
    new_node.ft = self.ft
    return new_node 
    
class Graph:
  def __init__(self, file_path):
    # Initizalize a graph with data read from a CSV file
    self.file_path = file_path
    self.original_graph_data = self.read_csv(file_path)
    self.graph_data = copy.deepcopy(self.original_graph_data)
    
  def read_csv(self, file_path):
    # Read data from a CSV file and create a Graph
    graph_data = {}
    try:
      with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # skip header row
        next(reader, None)
        
        for row in reader:
          if len(row) == 3: # Weighted graph
            source, target, weight = map(int, row)
            # skip any self-loops
            if source == target:
              continue
          elif len(row) == 2: # Unweighted graph
            source, target = map(int, row)
            weight = 1
            
          else: 
            print("Invalid number of columns in CSV file")
            return graph_data
          
          # Create Node objects for source and target
          if source not in graph_data:
            graph_data[source] = Node(source)
          if target not in graph_data:
            graph_data[target] = Node(target)

          graph_data[source].neighbors.append((graph_data[target], weight))
          graph_data[target].neighbors.append((graph_data[source], weight))
          
    except FileNotFoundError:
      print(f"Error: File not found at '{file_path}'")
    except Exception as e:
      print(f"An error ocurred: '{e}'")
    return graph_data
  
  def determine_graph_type(file_path):
    # DEtermine graph type based on the file name
    file_name = os.path.basename(file_path).lower()
    if "weighted" in file_name:
        if "undirected" in file_name:
            return "weighted_undirected"
        elif "directed" in file_name:
            return "weighted_directed"
        else:
            return "weighted"
    elif "unweighted" in file_name:
        if "undirected" in file_name:
            return "unweighted_undirected"
        elif "directed" in file_name:
            return "unweighted_directed"
        else:
            return "unweighted"
    elif "undirected" in file_name:
        return "undirected"
    elif "directed" in file_name:
        return "directed"
    else:
        return "unknown"
      
  def graph_data_copy(self):
    # Create a deep copy of the graph data
    return copy.copy(self.graph_data)

  def BFS(self, s_key):
    """ 
    Breath-First Search Algorithm to traverse a graph in the style of a breath.
    
    Time Complexity: Big-O (V + E), where V is the number of vertices and E is the number of edges.
    Space Complexity: Big-O(V), where V is the number of vertices.
    
    Parameters:
    - s_key: key for the starting vertex.
    
    Returns:
    - path: The dictionary of paths from the source vertex to all other vertices.
    """
    # Initialize attributes for all the nodes in the graph
    for u_key in self.graph_data:
      u = self.graph_data[u_key]
      u.color = "white"
      u.d = float('inf')
      u.pi = None
      
    # Retrieve the starting node using the provided key
    s = self.graph_data.get(s_key)
    if s is None:
      print(f"Error: Starting Vertex with key {s_key} not found in the graph")
      return
    
    # Set attributes for the starting node
    s.color = "grey"
    s.d = 0
    s.pi = None

    #Create empty queue
    Q = deque()
    Q.append(s)
    
    # Track the paths using node keys
    paths = {u.key: None for u in self.graph_data.values()}
    
    # Initialize the path for the starting node 
    paths[s.key] = [s.key]
    
    while Q:
      u = Q.popleft()
      for v_tuple in u.neighbors:
        v, _ = v_tuple
        if v.color == "white":
          v.color = "grey"
          v.d = u.d + 1
          v.pi = u
          Q.append(v)

          paths[v.key] = paths[u.key] + [v.key]

      u.color = "black"
      
    for vertex in self.graph_data.values():
        vertex.color = "white"

    return paths  

  def PrintPath(self, s_key, t_key, paths):
    # Prints the path from the source node to the target node if it exists
    node_s = self.graph_data.get(s_key)
    node_t = self.graph_data.get(t_key)
    
    if node_s is None or node_t is None:
      print("Node not found in the Graph.")
      return
    
    if s_key == t_key:
      print("Source and target are the same.")
      return
    
    if paths[t_key] is not None:
      path_nodes = [node for node in self.graph_data.values() if node.key in paths[t_key]]
      path = [node.key for node in path_nodes]
      print(f"Path from {node_s.key} to {node_t.key}: {' -> '.join(map(str, path))}")
    else:
      print(f"Path from {node_s.key} to {node_t.key} does not exists.")

  def DFS(self):
    """
    Depth-First Search Algorithm to traverse a graph in depth.
    
    Time Complexity: Big-O(V + E), where V is the number of vertices and E is the number of edges.
    Space Complexity: Big-O(V), where V is the number of vertices.
    """
    for u_key in self.graph_data:
      u = self.graph_data[u_key]
      u.color = "white"
      u.pi = None
    time = [0]

    for u_key in self.graph_data:
      u = self.graph_data[u_key]
      if u.color == "white":
        self.DFS_VISIT(u, time)
        
    for vertex in self.graph_data.values():
      vertex.color = "white"

  def DFS_VISIT(self, u, time):
    """""
    Recursive helper function for DFS.
    
    Parameters:
    - u: current node.
    - time: List to keep track of discovery and finish times.
    """
    u.color = "grey"
    time[0] += 1
    u.td = time[0]

    for v, _ in u.neighbors:
      if v.color == "white":
        v.pi = u
        self.DFS_VISIT(v, time)
    u.color = "black"
    time[0] += 1
    u.ft = time[0]
    
  def BFS_connected_components(self, s):
    """
    Implementation of BFS to find connected components in a graph.
    
    Parameters:
    - s: Starting vertex.
    
    Returns:
    - component: List of nodes contained in the connected tree or forest of connected trees.
    """
    component = []
    Q = deque()
    Q.append(s)
    s.color = "grey"

    while Q:
      u = Q.popleft()
      component.append(u)
      for v_tuple in u.neighbors:
        v, _ = v_tuple
        if v.color == "white":
            v.color = "grey"
            Q.append(v)
      u.color = "black"

    return component

  def connected_components(self):
    """ 
    Find all coonected components in the graph.
    
    Returns: 
    - components: List of connected components, each of which represent a list of nodes.
    - visited_nodes: keeps track of all the visited nodes.
    """
    components = []
    visited_nodes = set()
    for u in self.graph_data.values():
      if u.color == "white" and u.key not in visited_nodes:
        component = self.BFS_connected_components(u)
        components.append(component)
        
        for vertex in component:
          visited_nodes.add(vertex.key)
          
    # Sort components based on the minimum key of the nodes in each component
    components.sort(key = lambda comp: min(node.key for node in comp)) 
    return components


  def DFS_Cycle_Detection(self):
    """ 
    Implementation of DFS to detect cycles in a graph.
    
    Time Complexity: Big-O(V + E), where V is the number of vertices and E is the number of edges.
    Space Complexity: Big-O(V), where V is the number of vertices.
    
    Returns: 
    - has_cycle: True if the graph contains a cycle(s), False if the graph has no cycle(s).
    """
    for u_key in self.graph_data:
      u = self.graph_data[u_key]
      u.color = "white"
      u.pi = None
      
    for u_key in self.graph_data:
      u = self.graph_data[u_key]
      if u.color == "white":
        if self.DFS_Cycle_Detection_visit(u, None):
          return True

    return False

  def DFS_Cycle_Detection_visit(self, u, pi):
    """
    Recursive helper function for cycle detection.
    
    Parameters:
    - u: Current node.
    - pi: Parent node.
    
    Returns: 
    - has_cycle: True if the graph contains a cycle(s), False if the graph has no cycle(s).
    """
    u.color = "grey"

    for v_tuple in u.neighbors:
      v, _ = v_tuple
      if v.color == "white":
        v.pi = u
        if self.DFS_Cycle_Detection_visit(v, u) or v != pi:
          return True

    u.color = "black"
    return False

  def DFS_Topological(self):
    """
    Implementation of DFS to perform a Topological sort on a Directed Acyclic Graph (DAG).
    
    Time Complexity: Big-O(V + E), where V is the number of vertices and E is the number of edges.
    Space Complexity: Big-O(V), where V is the number of vertices.
    
    Returns: 
    - topological_order: List of vertices in topological order.
    """
    if self.DFS_Cycle_Detection(): # Checks if the Graph is a DAG
      print("The graph is not a Directed Acyclic Graph (DAG). Topological sort cannot be performed.")
      return []
    
    topological_order = []

    def DFS_Visit_Topological(u, time):
      nonlocal topological_order
      u.color = "grey"
      time[0] += 1
      u.td = time[0]

      for v_tuple in u.neighbors:
        v, _ = v_tuple
        if v.color == "white":
          v.pi = u
          DFS_Visit_Topological(v, time)

      u.color = "black"
      time[0] += 1
      u.ft = time[0]

      topological_order.insert(0, u.key)

    for u_key in self.graph_data:
      u = self.graph_data[u_key]
      if u.color == "white":
        time = [0]
        DFS_Visit_Topological(u, time)

    return topological_order

  def MST_Kruskal(self):
    """
    Kruskal's Algorithm to find the Minimum Spanning Tree (MST) of the graph.
    
    Time Complexity: Big-O(E log V), where V is the number of vertices and E is the number of edges.
    Space Complexity: Big-O(V), where V is the number of vertices.
    
    Returns: 
    - mst: List of edges forming the Minimum Spanning Tree.
    """
    edges = []
    for u_key in self.graph_data:
      u = self.graph_data[u_key]
      for v_tuple in u.neighbors:
        v, weight = v_tuple
        edges.append((weight, u.key, v.key))

    edges.sort()
    parent = {u: u for u in self.graph_data}

    def find_set(u):
      if parent[u] != u:
        parent[u] = find_set(parent[u])
      return parent[u]

    def union_set(u, v):
      u_root, v_root = find_set(u), find_set(v)
      parent[u_root] = v_root

    mst = []

    for edge in edges:
      weight, u, v = edge
      if find_set(u) != find_set(v):
        union_set(u, v)
        mst.append((u, v, weight))

    return mst
  
  def Dijkstra(self, s_key):
    """
    Dijkstra's Algorithm to find the shortest path from a source vertex to all other vertices.
    
    Time Complexity: Big-O((V + E) log V), where V is the number of vertices and E is the number of edges.
    Space Complexity: Big-O(V), where V is the number of vertices.
    
    Parameters:
    - s_key: Keey of the starting vertex.
    
    Returns: 
    - pi: Dictionary containing predecessors for each vertex in the shortest path.
    - d: Dictionary containting the shortest distance from the source vertex to each vertex.
    """
    s = self.graph_data.get(s_key)
    if s is None:
      print(f"Error: Starting Vertex with key {s_key} not found in the graph")
      return 
    
    d = {v.key: float('inf') for v in self.graph_data.values()}
    d[s.key] = 0
    pi = {v.key: None for v in self.graph_data.values()}
    visited = set()
    
    # Priority queue to store vertices based on their distance
    priority_queue = [(0, s.key, s)]
    
    while priority_queue:
      current_distance, current_key, u = heapq.heappop(priority_queue)
      
      if current_key in visited:
        continue
      
      visited.add(current_key)
      
      for v_tuple in u.neighbors:
        v, weight = v_tuple
        if v.key not in visited:
          if d[current_key] + weight < d[v.key]:
            d[v.key] = d[current_key] + weight
            pi[v.key] = current_key
            heapq.heappush(priority_queue, (d[v.key], v.key, v))
            
    return pi, d
  
  def Print_Dijkstra_Path(self, s_key, t_key, pi, d):
    # Print the shortest path found by Dijkstra's Algorithm
    node_s = self.graph_data.get(s_key)
    node_t = self.graph_data.get(t_key) 
    
    if node_s is None or node_t is None:
      print("Node not found in the Graph.")
      return
    
    path_nodes = []
    current_vertex_key = t_key
    
    while current_vertex_key is not None:
      current_vertex = self.graph_data[current_vertex_key]
      path_nodes.insert(0, current_vertex)
      current_vertex_key = pi[current_vertex_key]
      path = [(node.key, d[node.key]) for node in path_nodes]
      print(f"Shortest path from {node_s.key} to {node_t.key}: {path}")  
    
  def display_menu(self):
    # Prints to display the main menu
    print("Menu:")
    print("1. BFS")
    print("2. DFS")
    print("3. Connected Components")
    print("4. Cycle Detection")
    print("5. Topological Sort")
    print("6. MST Kruskal")
    print("7. Dijkstra")
    print("8. Exit")

  def menu_choice(self, choice):
    # Handleing the User's Menu Choices
    if choice == "1":
      print("You have selected BFS")
      # Prompts the user for the starting vertex and the target vertex
      source_vertex_key = int(input("Enter the key of the starting vertex: "))
      target_vertex_key = int(input("Enter the key of the target vertex: "))
      # Calls the BFS Algorithm and begins from the starting vertex provided
      paths = self.BFS(source_vertex_key)
      # Calls the print path function to print the path 
      self.PrintPath(source_vertex_key, target_vertex_key, paths)
      
    elif choice == "2":
      print("You have selected DFS")
      # Calls the DFS Algorithm
      self.DFS()
      for vertex_key in self.graph_data:
        vertex = self.graph_data[vertex_key]
        # Prints the discovery time and finish time of the vertexes
        print(f"Vertex {vertex.key}: Discovery time = {vertex.td}, Finish time = {vertex.ft}")
        
    elif choice == "3":
      print("You have selected Connected Components")
      # Calls the connected_components function and stores the values
      components = self.connected_components()
      for i, component in enumerate(components):
        vertices_str = ", ".join(str(vertex.key) for vertex in component)
        # Prints out the list of connected components
        print(f"Component {i + 1}: {[vertices_str]}")
        
    elif choice == "4":
      print("You have selected Cycle Detection")
      # Calls the DFS_Cycle_Detection function to verify if the graph has cycles
      has_cycle = self.DFS_Cycle_Detection()
      if has_cycle: # prints out a message saying if the graph has a cycle or not
        print("The Graph has a cycle.")
      else:
        print("The graph has no cycles.")
        
    elif choice == "5":
      print("You have selected Topological Sort")
      # Calls the DFS_Topological Algorithm to construct the topological sort if it is a DAG
      topological_order = self.DFS_Topological()
      print("Topological sort:",[vertex.key for vertex in topological_order])
      
    elif choice == "6":
      print("You have selected Kruskal's MST Algorithm")
      print(self.MST_Kruskal())
      
    elif choice == "7":
      print("You have selected Dijkstra's Shortest Path Algorithm")
      source_vertex_key = int(input("Enter the key of the starting vertex: "))
      target_vertex_key = int(input("Enter the key of the target vertex: "))
      
      pi, d = self.Dijkstra(source_vertex_key)
      self.Print_Dijkstra_Path(source_vertex_key, target_vertex_key, pi, d)
      
    elif choice == "8":
      print("You have selected to exit the program.")
      print("Now Exiting.")
      return True
    else:
      print("Invalid choice. Please try again.")
      return False

def main():
  # Main function to execute the program
  if len(sys.argv) != 2:
    print("Structure: python main.py <filepath>")
    sys.exit(1)
    
  file_path = sys.argv[1]
  # Check if the file exists
  if not os.path.exists(file_path):
    print(f"Error: File not found in file path  '{file_path}'")
    sys.exit(1)
    
  # Determine the graph type from the file path
  graph_type =  Graph.determine_graph_type(file_path)
  
  if graph_type not in ["weighted", "unweighted", "directed", "undirected"]:
    print("Invalid graph type")
    sys.exit(1)
    
  graph = Graph(file_path)
  
  # while loop for the menu
  while True:
    # Display menu
    graph.display_menu()

    choice = input("Enter your choice: ")
    exit_menu = graph.menu_choice(choice)
    
    if exit_menu:
      break

if __name__ == "__main__":
  main()