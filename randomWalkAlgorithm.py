import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import random

def randomWalkAlgorithm(nodeId, resourceId, ttl, graph, visited, msgNumber, cache=False, parent = -1, path=""):
    strInicial = "" if parent == -1 else "-> "
    newPath = path+f"{strInicial}{nodeId} "

    msgNumber+=1

    if visited[nodeId]:
        return -2, msgNumber # JA FOI VISITADO
    
    print()
    visited[nodeId] = True

    if resourceId in graph[nodeId].resources:
        print(f"{newPath}\nttl:{ttl}\tRecurso encontrado!")
        return nodeId, msgNumber

    if cache and resourceId in graph[nodeId].cashe.keys():
        cacheOnNode = graph[nodeId].cashe[resourceId]
        print(f"{newPath}\nttl:{ttl}\tSe encontra no cache no nó: {cacheOnNode}")
        return cacheOnNode, msgNumber
    

    if ttl == 0:
        print(f"{newPath}\nttl:{ttl}\tRecurso Nao encontrado")
        return -1, msgNumber # RECURSO NAO ENCONTRADO
    

    neighbors = graph[nodeId].connections
    while neighbors:
        neighbor = neighbors.pop(random.randint(0,len(neighbors)-1))
        
        if neighbor == parent:
            continue

        print(f"{newPath}\nttl:{ttl}\tRecurso Nao encontrado, ->{neighbor}")
    
        result, msgNumber = randomWalkAlgorithm(neighbor, resourceId, ttl-1, graph, visited, msgNumber, cache, nodeId, newPath)

        if result >= 0:
            if cache:
                graph[nodeId].cashe[resourceId] = result
            return result, msgNumber
        elif result < 0:
            print()

    print(f"{newPath}\nttl:{ttl}\tRecusor nao encontrado, caminho ja visitado")

    return -1, msgNumber


def visualizeRandomWalk(graph, path):
    graph_nx = nx.Graph()
    for i, device in enumerate(graph):
        graph_nx.add_node(i)
        for neighbor in device.connections:
            graph_nx.add_edge(i, neighbor)

    pos = nx.spring_layout(graph_nx)

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['lightblue'] * len(graph)

    # Função para atualizar os quadros da animação
    def update(frame):
        if frame < len(path):
            node, ttl = path[frame]
            colors[node] = 'orange' if frame < len(path) - 1 else 'green'
            ax.clear()
            nx.draw(graph_nx, pos, ax=ax, with_labels=True, node_color=colors, font_weight='bold')
            ax.text(0.05, 0.95, f"TTL: {ttl}", transform=ax.transAxes, fontsize=12, verticalalignment="top")
            ax.text(0.05, 0.90, f"Step: {frame + 1}", transform=ax.transAxes, fontsize=12, verticalalignment="top")

    anim = FuncAnimation(fig, update, frames=len(path), interval=1000, repeat=False)
    plt.show()
