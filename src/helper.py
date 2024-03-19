'''
This file contains helper functions for the simulation
Functions are:
    - DFS: Depth First Search traversal of any graph
    - connectedComponents: find clusters in a graph
    - visualize_graph: visualize the graph
    - exponential_sample: return value from an exponential sample
    - uniform_sample: return value from an uniform sample
    - create_random_transaction: create an empty or non empty transaction based on initial state
    - generate_Tk: generate mining time for any peer
    - validate_block: validate the block based on balance 
    - traverse_and_add: traverse the tree and add block to tail or non tail
    - find_longest_tail: find the longest tail in the tail list

'''
import random
import networkx as nx
import matplotlib.pyplot as plt

# Courtesy: https://www.geeksforgeeks.org
# DFS traversal of any graph
def DFS(G, temp, v, visited):
    visited[v] = True
    temp.append(v)
    neighbours = list(G.neighbors(v))
    for neighbour in neighbours:
        if visited[neighbour] == False:
            temp = DFS(G, temp, neighbour, visited)
    return temp

# Courtesy: https://www.geeksforgeeks.org
# find clusters in a graph
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

# Courtesy: Documentation of NetworkX drawing
# visualize the graph
def visualize_graph(G, figure_no):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=100, node_color="skyblue", font_size=8,
            font_color="black", font_weight="bold", edge_color="gray", linewidths=0.5)
    plt.savefig(f'../figs/fig{figure_no}.png')
    plt.clf()

# Courtesy: Generative AI
# return value from an exponential sample
def exponential_sample(mean):
    return random.expovariate(1 / mean)

# return value from an uniform sample
def uniform_sample(low, high):
    return random.uniform(low, high)

# create an empty or non empty transaction based on initial state
def create_random_transaction(num_of_peers, initial_state = False):
    payer = random.randint(0, num_of_peers - 1)
    payee = random.randint(0, num_of_peers - 1)
    if initial_state:
        coins = 0
    else:
        coins = random.randint(1, 10)
    return payer, payee, coins

# generate mining time for any peer
def generate_Tk(peer, interval = 600):
        if peer.hashpower == 0 : 
            mean = interval / 1e-9
        else:
            mean = interval / peer.hashpower
        Tk = exponential_sample(mean)
        return Tk

# validate the block based on balance 
def validate_block(block):
    for txn in block.transactions:
        if txn.payer.balance < txn.coins:
            return False
    return True

# traverse the tree and add block to tail or non tail
def traverse_and_add(peer, block):
    print(f"debug prev={block.prevblockid}, peer={peer.id}, block-{block.id}")
    found = False
    should_form = False
    for tail in peer.taillist:
        if tail.block.id == block.prevblockid:
            found = True
            break
    if found:
        should_form = peer.add_block_to_tail(block, tail)
        print(f"added to tail{block.id}")
    else:
        current_tails = peer.taillist
        parent = None
        for tail in current_tails:
            while tail.prevNode != None:
                if tail.prevNode.block.id == block.prevblockid:
                    parent = tail.prevNode
                    break
                else:
                    tail = tail.prevNode
        peer.add_block_to_nontail(block, parent)
        print(f"added to non-tail{block.id}")
    print(peer.print_whole_tree())
    
    return should_form

def find_longest_tail(taillist) :
    return max(taillist, key=taillist.get)

def is_selfish(peer):
    if peer.id in [0,1]:
        return True
    return False