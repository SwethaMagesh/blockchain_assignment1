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
        coins = 0
    else:
        coins = random.randint(1, 10)
    return payer, payee, coins


def generate_Tk(peer, interval = 600):
        mean = interval / peer.hashpower
        Tk = random.expovariate(1/mean)
        print(f"will wait for {Tk} seconds")
        return Tk

def validate_block(block):
    # every transaction of block should be valid
    for txn in block.transactions:
        if txn.payer.balance < txn.coins:
            return False
    return True

def traverse_and_add(peer, block):
    # if block.prevblockid is that of the taillist add
    print(f"Traversing and adding block {block.id} to peer {peer.id}")
    found = False
    should_form = False
    for tail in peer.taillist:
        if tail.block.id == block.prevblockid:
            found = True
            break
    if found:
        should_form = peer.add_block_to_tail(block, tail)
    else:
        print(f"Block {block.id} is not a tail block")
        for tail in peer.taillist:
            if tail.prevNode != None:
                if tail.prevNode.block.id == block.prevblockid:
                    peer.add_block_to_nontail(block, tail.prevNode)
                    break
    return should_form
            
            
    