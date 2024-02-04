import argparse
from blockchain import *
import networkx as nx
import random
import matplotlib.pyplot as plt
from peer import *
from block import *
from transaction import *
import simpy
import time



parser = argparse.ArgumentParser(description="command line argument parser")

# number of peers in the network
parser.add_argument("--peers", "-n", type=int, default=10, required=True, help="enter the number of peers in the network")
# number of slow peers in the network
parser.add_argument("--slow", "-z0", type=float, default=0.3, required=True, help="enter the number of slow peers in the network")
# number of lowCPU peers in the network
parser.add_argument("--low", "-z1", type=float, default=0.3, required=True, help="enter the number of lowCPU peers in the network")
#  inter arrival time of transactions
parser.add_argument("--txninterval", "-Ttx", type=float, default=5, required=True, help="enter the inter arrival time of transactions")
#  inter arrival time of blocks
parser.add_argument("--blockinterval", "-I", type=float, default=10, required=True, help="enter the inter arrival time of blocks")

args = parser.parse_args()
n_peers = args.peers
z0_slow = args.slow
z1_low = args.low
I_txn = args.txninterval
I_block = args.blockinterval

# local printing
print("peers in network        = ", n_peers)
print("fraction slow peers     = ", z0_slow)
print("fraction low CPU peers  = ", z1_low)
print("transaction interval    = ", I_txn)
print("block interval          = ", I_block)



# Constants
TRANSACTION_SIZE = 1 # in KB
MAX_BLOCK_SIZE = 1024 # in KB
START_TIME = 0

# generate a random graph with n peers and parameters
G = nx.Graph()

def generate_random_graph(n_peers, z0_slow, z1_low):
    for peer in range(n_peers):
        G.add_node(peer)
    for node in G.nodes():
        degree = random.randint(3,6)
        while G.degree(node) < degree:
            possible_nodes = [other_node for other_node in G.nodes() if other_node != node and G.degree(other_node) < 6]
            if len(possible_nodes) == 0:
                break
            other_node = random.choice(possible_nodes)
            G.add_edge(node, other_node)

    # randomly allocate nodes as slow or lowcpu
    slow_peers = random.sample(range(n_peers), int(z0_slow * n_peers))
    lowcpu_peers = random.sample(range(n_peers), int(z1_low * n_peers))

    # calculate hashpower of slow and fast nodes
    slow_hashpower = 1 / (10 - 9*z1_low)
    fast_hashpower = 10 * slow_hashpower

    # populate peers with their parameters
    peers = []
    for peer in range(n_peers):
        if peer in slow_peers:
            slow = True
        else:
            slow = False
        if peer in lowcpu_peers:
            lowcpu = True
            hashpower = slow_hashpower
        else:
            lowcpu = False
            hashpower = fast_hashpower
        peers.append(Peer(peer, slow=slow, lowcpu=lowcpu, hashpower=hashpower))

    # populate links with their parameters
    links = {} 
    for i, j in G.edges():
        ro = random.randrange(10, 500)
        if peers[i].slow  or peers[j].slow:
            speed = 5
        else:
            speed = 100
        if i in links:
            links[i][j] = Link(i, j, speed, ro)
        else:
            links[i] = {j: Link(i, j, speed, ro)}

    # local printing
    print("Edges : ")
    print(G.edges())
    print("Nodes : ")
    print(G.nodes())
    print("Degree : ")
    for node in G.nodes():
        print(G.degree(node), end=" ")
    print("\nSlow Peers : ")
    print(slow_peers)
    print("Low CPU Peers : ")
    print(lowcpu_peers)
    print("Peers : ")
    for i in peers:
        print(i)
    print("Links : ")
    for _, neighbor_link in links.items():
        for _, link_obj in neighbor_link.items():
            print(link_obj)
    # visualize graph
    # pos = nx.spring_layout(G)  
    # nx.draw(G, pos, with_labels=True, node_size=100, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", edge_color="gray", linewidths=0.5)
    # plt.show()
    return peers, links

# generate random graph
peers, links = generate_random_graph(n_peers, z0_slow, z1_low)

RANDOM_SEED = int(time.time())
SIM_TIME = 20

random.seed(RANDOM_SEED)
env = simpy.Environment()

txn = Transaction(sender=peers[2], receiver=peers[8], coins=0)

env.process(forward_transaction(peers[2], txn, peers[2], env))