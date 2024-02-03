import networkx as nx
import random
import matplotlib.pyplot as plt
from peer import Peer, Link

# BLOCKCHAIN SIMULATION 
# Constants

TRANSACTION_SIZE = 1 # in KB
MAX_BLOCK_SIZE = 1024 # in KB
START_TIME = 0


def generate_random_graph(num_of_nodes, z_slow, z1_slowcpu):
    # generate a random graph with n peers and parameters

    G = nx.Graph()
    for i in range(num_of_nodes):
        G.add_node(i)
    for n in G.nodes():
        deg = random.randint(3,6)
        while G.degree(n) < deg:
            possible_nodes = [node for node in G.nodes() if node != n and G.degree(node) < 6]
            if len(possible_nodes) == 0:
                break
            m = random.choice(possible_nodes)
            G.add_edge(n, m)

    print(G.edges())
    print(G.nodes())
    for i in G.nodes():
        print(G.degree(i))
    pos = nx.spring_layout(G)  # You can use other layouts as well
    nx.draw(G, pos, with_labels=True, node_size=100, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", edge_color="gray", linewidths=0.5)

    # Display the graph
    plt.show()

    peers = []
    links = []


    
    slow_nodes = int(z_slow*num_of_nodes)
    slowcpu_nodes = int(z1_slowcpu*num_of_nodes)
    random_slow = random.sample(range(num_of_nodes), slow_nodes)
    random_slowcpu = random.sample(range(num_of_nodes), slowcpu_nodes)

    print(random_slow)
    print(random_slowcpu)

    slow_hashpower = 1/ (10 - 9*z1_slowcpu)
    high_hashpower = 10*slow_hashpower



    for i in range(num_of_nodes):
        if i in random_slow:
            slow = True
        else:
            slow = False
        if i in random_slowcpu:
            slowcpu = True
            hashpower = slow_hashpower
        else:
            slowcpu = False
            hashpower = high_hashpower
        peers.append(Peer(i, slow=slow, slowcpu=slowcpu, hashingpower=hashpower))
        
    
    for i,j in G.edges():

        if peers[i].slow  or peers[j].slow:
            ro = random.randrange(10, 500)
            link = Link(i,j,5, ro)
        else:
            ro = random.randrange(1, 10)
            link = Link(i,j,100, ro)
        links.append(link)




    for i in peers:
        print(i)
    for i in links:
        print(i)

    return peers, links

    




