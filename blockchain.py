import networkx as nx
import random
import matplotlib.pyplot as plt
from peer import Peer, Link
from block import Block

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
    links = []  
    for i, j in G.edges():
        if peers[i].slow  or peers[j].slow:
            ro = random.randrange(10, 500)
            link = Link(i, j, 5, ro)
        else:
            ro = random.randrange(1, 10)
            link = Link(i, j, 100, ro)
        links.append(link)

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
    for i in links:
        print(i)
    # visualize graph
    # pos = nx.spring_layout(G)  
    # nx.draw(G, pos, with_labels=True, node_size=100, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", edge_color="gray", linewidths=0.5)
    # plt.show()
    b1 = Block()
    dij = b1.generate_qdelay(links[1])
    print("Queueing Delay of Peer \"", links[1], "\" = ", dij)
    return peers, links