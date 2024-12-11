import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation

def floodingAlgorithm(nodeId, resourceId, ttl, graph, visited, msgNumber, cache=False):
    parent = [-1 for _ in graph]
    queue = [[nodeId, ttl]]
    result = -1

    while queue:
        current, current_ttl = queue.pop(0)
        msgNumber += 1

        if visited[current]:
            continue
        visited[current] = True

        parent_str = "Comeco da busca, Nó: " if parent[current] == -1 else f"Pai: {parent[current]} > "
        if resourceId in graph[current].resources:
            print(f"{parent_str}{current}\tttl:{current_ttl}\tRecurso encontrado!")
            print()
            result = current

            if cache:
                for i,x in enumerate(visited):
                    if x:
                        graph[i].cache[resourceId] = result

            continue

        if cache and resourceId in graph[current].cache.keys():
            print(f"{parent_str}{current}\tttl:{current_ttl}\tSe encontra no cache no nó: {graph[current].cache[resourceId]}")
            print()
            result =  graph[current].cache[resourceId]

            for i,x in enumerate(visited):
                if x:
                    graph[i].cache[resourceId] = result

            continue

        if current_ttl == 0:
            print(f"{parent_str}{current}\tttl:{current_ttl}\tRecurso Nao encontrado")
            print()
            continue

        child_neighbors = []
        for neighbor in graph[current].connections:
            if parent[neighbor] == -1:
                parent[neighbor] = current

            if neighbor != parent[current]:
                queue.append([neighbor,current_ttl-1])
                child_neighbors.append(neighbor)
        
        print(f"{parent_str}{current}\tttl:{current_ttl}\tRecurso Nao encontrado, vizinhos do filho -> {child_neighbors}")
        print()

    return result, msgNumber


def visualizeFlooding(graph, visited_order):
    graph_nx = nx.Graph()
    for i, device in enumerate(graph):
        graph_nx.add_node(i)
        for neighbor in device.connections:
            graph_nx.add_edge(i, neighbor)

    pos = nx.spring_layout(graph_nx)

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['lightblue'] * len(graph)

    def update(frame):
        if frame < len(visited_order):
            node, ttl = visited_order[frame]
            colors[node] = 'orange' if frame < len(visited_order) - 1 else 'green'
            ax.clear()
            nx.draw(graph_nx, pos, ax=ax, with_labels=True, node_color=colors, font_weight='bold')
            ax.text(0.05, 0.95, f"TTL: {ttl}", transform=ax.transAxes, fontsize=12, verticalalignment="top")

    anim = FuncAnimation(fig, update, frames=len(visited_order), interval=1000, repeat=False)
    plt.show()
