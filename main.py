import json
from floodingAlgorithm import floodingAlgorithm
from randomWalkAlgorithm import randomWalkAlgorithm

class Device :
    def __init__(self, resources, connections):
        self.resources = resources
        self.connections = connections
        self.cache = {}

data = {}
graph = []

with open('settings.json', 'r') as file:
    data = json.load(file)

if len(data['edges']) != data["num_nodes"]:
    raise ValueError(f"Edges: rede possui {len(data['edges'])} dispositivos ao inves de {data['num_nodes']}")

if len(data['resources']) != data["num_nodes"]:
    raise ValueError(f"Resources: rede possui {len(data['resources'])} dispositivos ao inves de {data['num_nodes']}")

graph = [Device(data["resources"][i], data["edges"][i]) for i in range(data["num_nodes"])]

for i, device in enumerate(graph):
    if len(device.connections) == 0:
        raise ValueError(f"dispositivo {i} não possui conexões")
    
    if len(device.connections) < data["min_neighbors"]:
        raise ValueError(f"dispositivo {i} possui menos conexões que o limite")

    if len(device.connections) > data["max_neighbors"]:
        raise ValueError(f"dispositivo {i} possui mais conexões que o limite")

    for x in device.connections:
        if x == i:
            raise ValueError(f"dispositivo {i} está apontando para ele mesmo")

        if not i in graph[x].connections:
            raise ValueError(f"dispositivo {i} se conecta ao dispositivo {x}. Porém, {x} não se conecta a {i}")

    if len(device.resources) == 0:
        raise ValueError(f"dispositivo {i} não possui recursos")

def start_search(nodeId, resourceId, ttl, algorithm, visualize=False):
    print(f"\nalgoritimo \033[4m{algorithm}\033[0m selecionado")
    print()

    visited = [False for _ in graph]
    msgNumber = -1
    if algorithm == "f":
        value, msgNumber = floodingAlgorithm(nodeId, resourceId, ttl, graph, visited, msgNumber)
        # if visualize:
        #     visualizeFlooding(graph, visited_order)

    elif algorithm == "rw":
        value, msgNumber = randomWalkAlgorithm(nodeId, resourceId, ttl, graph, visited, msgNumber)
        # if visualize:
        #     visualizeRandomWalk(graph, path)
    
    elif algorithm == "fc":
        value, msgNumber = floodingAlgorithm(nodeId, resourceId, ttl, graph, visited, msgNumber, True)

    elif algorithm == "rwc":
        value, msgNumber = randomWalkAlgorithm(nodeId, resourceId, ttl, graph, visited, msgNumber, True)

    if value == -1:
        print("\n recurso não encontrado ")
    
    print("numero de mensagens trocadas: ", msgNumber)
    print("nós envolvidos na busca: ", sum(visited))

def main_loop():
    print("\n=== Busca em Rede com Algoritmos de Flooding e Random Walk ===\n")
    print("Escolha um algoritmo:")
    print(f"1 - Flooding (f)")
    print(f"2 - Random Walk (rw)")
    print(f"3 - Flooding com cache (fc)")
    print(f"4 - Random Walk com cache (rwc)")
    print("Digite 'exit' para sair.")

    while True:
        algorithm = input("\nEscolha o algoritmo (f, rw, fc, rwc): ").strip().lower()
        if algorithm == "exit":
            print("Encerrando o programa. Até mais!")
            break

        try:
            nodeId = int(input(f"Digite o ID do nó inicial (0 a {data["num_nodes"] - 1}): "))
            resourceId = input("Digite o ID do recurso: ").strip()
            ttl = int(input("Digite o TTL: "))

            if algorithm not in ["f", "rw", "fc", "rwc"]:
                raise ValueError("Algoritmo inválido. Escolha uma das opções fornecidas.")

            start_search(nodeId, resourceId, ttl, algorithm)

        except ValueError as e:
            print(f"Erro: {e}. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main_loop()
