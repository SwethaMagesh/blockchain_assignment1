import random
import networkx as nx
import matplotlib.pyplot as plt

def DFS(G, temp, v, visited):
    visited[v] = True
    temp.append(v)
    neighbours = list(G.neighbors(v))
    for neighbour in neighbours:
        if visited[neighbour] == False:
            temp = DFS(G, temp, neighbour, visited)
    return temp

def connectedComponents(G, n_peers):
    visited = []
    cluster = []
    for _ in range(n_peers):
        visited.append(False)
    for v in range(n_peers):
        if visited[v] == False:
            temp= []
            cluster.append(DFS(G, temp, v, visited))
    return cluster


def visualize_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=100, node_color="skyblue", font_size=8,
            font_color="black", font_weight="bold", edge_color="gray", linewidths=0.5)
    plt.show()

def exponential_sample(mean):
    return random.expovariate(1 / mean)

def uniform_sample(low, high):
    return random.uniform(low, high)

def create_random_transaction(num_of_peers, initial_state = False):
    payer = random.randint(0, num_of_peers - 1)
    payee = random.randint(0, num_of_peers - 1)
    if initial_state:
        coins = random.randint(0,1)
    coins = random.randint(1, 10)
    return payer, payee, coins


def generate_Tk(peer, interval = 600):
        mean = interval / peer.hashpower
        Tk = random.expovariate(1 / mean)
        return Tk
