import argparse
import networkx as nx
import random
from classes import *
import simpy
import time


parser = argparse.ArgumentParser(description="command line argument parser")

# number of peers in the network
parser.add_argument("--peers", "-n", type=int, default=10,
                    required=True, help="enter the number of peers in the network")
# number of slow peers in the network
parser.add_argument("--slow", "-z0", type=float, default=0.3,
                    required=True, help="enter the number of slow peers in the network")
# number of lowCPU peers in the network
parser.add_argument("--low", "-z1", type=float, default=0.3, required=True,
                    help="enter the number of lowCPU peers in the network")
#  inter arrival time of transactions
parser.add_argument("--txninterval", "-Ttx", type=float, default=5,
                    required=True, help="enter the inter arrival time of transactions")
#  inter arrival time of blocks
parser.add_argument("--blockinterval", "-I", type=float, default=10,
                    required=True, help="enter the inter arrival time of blocks")

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
TRANSACTION_SIZE = 1  # in KB
MAX_BLOCK_SIZE = 1024  # in KB
START_TIME = 0

# generate a random graph with n peers and parameters
G = nx.Graph()

def generate_random_graph(n_peers, z0_slow, z1_low):
    for peer in range(n_peers):
        G.add_node(peer)
    for node in G.nodes():
        degree = random.randint(3, 6)
        while G.degree(node) < degree:
            possible_nodes = [other_node for other_node in G.nodes(
            ) if other_node != node and G.degree(other_node) < 6]
            if len(possible_nodes) == 0:
                break
            other_node = random.choice(possible_nodes)
            G.add_edge(node, other_node)
    
    # make the graph connected
    clusters = connectedComponents(G,n_peers)
    print(f"Clusters in the graph are {len(clusters)}")
    visualize_graph(G)
    if len(clusters) != 1:
        for i in range(len(clusters)-1):
            node = random.choice(clusters[i])
            other_node = random.choice(clusters[i+1])
            G.add_edge(node, other_node)
    clusters = connectedComponents(G,n_peers)
    print(f"Clusters in the graph are {len(clusters)}")
    visualize_graph(G)

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
        if peers[i].slow or peers[j].slow:
            speed = 5
        else:
            speed = 100
        if i in links:
            links[i][j] = Link(i, j, speed, ro)
        else:
            links[i] = {j: Link(i, j, speed, ro)}
        if j in links:
            links[j][i] = Link(j, i, speed, ro)
        else:
            links[j] = {i: Link(j, i, speed, ro)}

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
    
    return peers, links


# generate random graph
peers, links = generate_random_graph(n_peers, z0_slow, z1_low)



def handle_transaction(env):
    yield env.timeout(exponential_sample(I_txn))
    s, r, c = create_random_transaction(n_peers, initial_state=True)
    txn = Transaction(payer=peers[s], payee=peers[r], coins=c)
    print(f"Created T{txn.txnid} at time {env.now}")
    payer = peers[s]
    receive_transaction(payer, payer, txn, env)
    env.process(forward_transaction(txn, payer, payer, env))


# receive transaction from peers
def receive_transaction(peer, hears_from, transaction, env):
    print(f"Peer {peer.id} recvs from {hears_from.id} T{transaction.txnid} at time {env.now}")
    if transaction.txnid not in [txn.txnid for txn in peer.transactions_queue]:
        peer.transactions_queue.append(transaction)


def forward_transaction(transaction, curr_peer, prev_peer, env):
    print(f"T{transaction.txnid} has already been sent by {transaction.sent_peers}")
    if curr_peer.id in transaction.sent_peers:
        print(f"Peer {curr_peer.id} already sent T{transaction.txnid}")
        return
    else:
        transaction.sent_peers.add(curr_peer.id)
        neighbours = list(links[curr_peer.id].keys())
        print(f"Peer {curr_peer.id} sends to neighbours {neighbours}")

        for neighbour in neighbours:
            if (neighbour != prev_peer.id) :
                print(f"Peer {curr_peer.id} sends to   {neighbour}  T{transaction.txnid} at time {env.now}")
                link = links[curr_peer.id][neighbour]
                yield env.timeout(transaction.generate_qdelay(link))
                receive_transaction(peers[neighbour], curr_peer, transaction, env)
                env.process(forward_transaction(transaction, peers[neighbour], curr_peer, env))

def forward_block(block, curr_peer, prev_peer, env):
    print(f"B{block.id} has already been sent by {block.sent_peers}")
    if curr_peer.id in block.sent_peers:
        print(f"Peer {curr_peer.id} already sent B{block.id}")
        return
    else:
        block.sent_peers.add(curr_peer.id)
        neighbours = list(links[curr_peer.id].keys())
        print(f"Peer {curr_peer.id} sends to neighbours {neighbours}")

        for neighbour in neighbours:
            if (neighbour != prev_peer.id) :
                print(f"Peer {curr_peer.id} sends to   {neighbour}  B{block.id} at time {env.now}")
                link = links[curr_peer.id][neighbour]
                yield env.timeout(block.generate_qdelay(link))
                receive_block(peers[neighbour], curr_peer, block, env)
                env.process(forward_transaction(block, peers[neighbour], curr_peer, env))
        

def mine_block(peer, env):
    block = Block()
    block.form_block(peer)
    print(f"Peer {peer.id} forms B{block.id} at time {env.now}")
    yield env.timeout(generate_Tk(peer, 10))
    peer.add_block_to_tail(block)
    print(f"{peer.id} 's Tree =>  {peer.tree.print_tree()}")
    # env.process(forward_block(peer, block, env))
    # env.process(validate_block(peer, block, env))
    # env.process(receive_block(peer, block, env))

RANDOM_SEED = int(time.time())
SIM_TIME = 20

random.seed(RANDOM_SEED)
env = simpy.Environment()
genesis = Block()
genesis_node = TreeNode(genesis, None)
for i in range(n_peers):
    peers[i].tree = genesis_node
    peers[i].blockids.append(genesis.id)
    peers[i].taillist[genesis_node] = 0

for i in range(10):
    env.process(handle_transaction(env))

for i in range(10):
    env.process(mine_block(peers[i], env))


env.run(until=SIM_TIME)
