'''
Flow of simulation is as follows:
    - Generate a random graph with n peers and parameters
    - Create and forward transactions
    - Create, forward and receive blocks
    - Visualize trees for any 5 peers
'''
import subprocess
import argparse
import networkx as nx
import random
import simpy
import time
import logging
from classes import *

# setup logging information file
logging.basicConfig(filename="../logs/blockchain.log", format='%(message)s', filemode='w')
logger = logging.getLogger('main.py')
logger.setLevel(logging.DEBUG)

# Courtesy: https://docs.python.org/3/library/argparse.html
# parse command line arguments n, z0, z1, Ttx, I
parser = argparse.ArgumentParser(description="command line argument parser")
# number of peers in the network
parser.add_argument("--peers", "-n", type=int, default=10,required=True, help="enter the number of peers in the network")
# number of slow peers in the network
parser.add_argument("--slow", "-z0", type=float, default=0.3,required=True, help="enter the number of slow peers in the network")
# number of lowCPU peers in the network
parser.add_argument("--low", "-z1", type=float, default=0.3, required=True,help="enter the number of lowCPU peers in the network")
#  inter arrival time of transactions
parser.add_argument("--txninterval", "-Ttx", type=float, default=5,required=True, help="enter the inter arrival time of transactions")
#  inter arrival time of blocks
parser.add_argument("--blockinterval", "-I", type=float, default=10,required=True, help="enter the inter arrival time of blocks")
#  hashing power of selfish miner 1
parser.add_argument("--zeta1", "-a1", type=float, default=10,required=True, help="enter the hashing power of selfish miner 1")
#  hashing power of selfish miner 2
parser.add_argument("--zeta2", "-a2", type=float, default=10,required=True, help="enter the hashing power of selfish miner 1")

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
figure_no = 0

def generate_random_graph(n_peers, z0_slow, z1_low):
    # add all peers as nodes
    for peer in range(n_peers):
        G.add_node(peer)
    # add edges b/w random nodes with degrees in {3...6}
    for node in G.nodes():
        degree = random.randint(3, 6)
        while G.degree(node) < degree:
            possible_nodes = [other_node for other_node in G.nodes() if other_node != node and G.degree(other_node) < 6]
            if len(possible_nodes) == 0:
                break
            other_node = random.choice(possible_nodes)
            G.add_edge(node, other_node)

    # make the graph connected by randomly adding an edge b/w two clusters
    clusters = connectedComponents(G, n_peers)
    if len(clusters) != 1:
        for i in range(len(clusters)-1):
            node = random.choice(clusters[i])
            other_node = random.choice(clusters[i+1])
            G.add_edge(node, other_node)
    clusters = connectedComponents(G, n_peers)

    # randomly allocate nodes as slow or lowcpu
    slow_peers = random.sample(range(n_peers), int(z0_slow * n_peers))
    lowcpu_peers = random.sample(range(n_peers), int(z1_low * n_peers))

    # calculate hashpower of slow and fast nodes
    slow_hashpower = 1 / ((10 - 9*z1_low)*n_peers)
    fast_hashpower = 10 * slow_hashpower

    # populate peers with their parameters
    peers = []
    for peer in range(n_peers):
        if peer in slow_peers:
            is_slow = True
        else:
            is_slow = False
        if peer in lowcpu_peers:
            is_lowcpu = True
            hashpower = slow_hashpower
        else:
            is_lowcpu = False
            hashpower = fast_hashpower
        peers.append(Peer(peer, slow=is_slow, lowcpu=is_lowcpu, hashpower=hashpower))

    # populate links with their parameters
    links = {}
    for i, j in G.edges():
        ro = uniform_sample(10,500)
        if peers[i].is_slow or peers[j].is_slow:
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

    # visulaize th network
    global figure_no
    figure_no = 999
    visualize_graph(G, figure_no)
    return peers, links

# create and forward transactions from here
def handle_transaction(env):
    yield env.timeout(exponential_sample(I_txn))
    # set the initial state to False ONLY after a few blocks have been mined
    initial_state = True if env.now < 100 else False
    s, r, c = create_random_transaction(n_peers, initial_state=initial_state)
    txn = Transaction(payer=peers[s], payee=peers[r], coins=c)
    peers[s].balance -= c
    peers[r].balance += c
    logger.debug(f"{env.now} P{peers[s].id} creates T{txn.id}")
    payer = peers[s]
    # payer adds this txn to its own queue and then forwards it
    receive_transaction(payer, payer, txn, env)
    env.process(forward_transaction(txn, payer, payer, env))

# receive transaction from peers
def receive_transaction(peer, hears_from, transaction, env):
    if transaction.id not in [txn.id for txn in peer.transactions_queue]:
        peer.transactions_queue.append(transaction)

def forward_transaction(transaction, curr_peer, prev_peer, env):
    # return if txn has already been processed
    if curr_peer.id in transaction.sent_peers:
        return
    else:
        # forward the txn to the current peer's neighbours
        transaction.sent_peers.add(curr_peer.id)
        neighbours = list(links[curr_peer.id].keys())
        for neighbour in neighbours:
            # do not re-forward to the peer from where it was received
            if (neighbour != prev_peer.id):
                link = links[curr_peer.id][neighbour]
                # simulate network delays
                yield env.timeout(transaction.generate_qdelay(link))
                receive_transaction(peers[neighbour], curr_peer, transaction, env)
                env.process(forward_transaction(transaction, peers[neighbour], curr_peer, env))

# forward blocks similar to transactions
def forward_block(block, curr_peer, prev_peer, env):
    if curr_peer.id in block.sent_peers:
        return
    else:
        block.sent_peers.add(curr_peer.id)
        neighbours = list(links[curr_peer.id].keys())
        for neighbour in neighbours:
            if (neighbour != prev_peer.id):
                link = links[curr_peer.id][neighbour]
                delay = block.generate_qdelay(link)
                yield env.timeout(delay)
                receive_block(peers[neighbour], curr_peer, block, env)
                env.process(forward_block(block, peers[neighbour], curr_peer, env))

# receive block from peers
def receive_block(peer, hears_from, block, env):
    logger.debug(f"{env.now} P{peer.id} recvs B{block.id} from P{hears_from.id}")
    # if block is not already processed, validate it
    if block.id not in peer.blockids:
        isvalid = validate_block(block)
        should_form = False
        if isvalid:
            # add to tree if parent block is found
            if block.prevblockid in peer.blockids:
                should_form = traverse_and_add(peer, block)
                logger.debug(f"{env.now} P{peer.id} adds B{block.id} to its tree")
            # add to pending queue if parent block is not found
            else:
                logger.debug(f"{env.now} P{peer.id} adds B{block.id} to its pending queue")
                peer.pending_blocks_queue.append(block)
            # start mining a new block if current block is added to the longest chain
            if should_form:
                env.process(mine_block(peer, env))

# mining process of a new block
def mine_block(peer, env):
    longest_tail = find_longest_tail(peer.taillist)
    mining_time = generate_Tk(peer, I_block)
    # start mining
    logger.debug(f"{env.now} P{peer.id} mines for {mining_time} seconds")
    yield env.timeout(mining_time)
    # stop mining and find the current longest chain
    longest_tail_new = find_longest_tail(peer.taillist)
    # if the longest chain is the same, create a new block
    if longest_tail_new == longest_tail:
        block = Block()
        if block.form_block(peer):
            peer.add_block_to_tail(block, longest_tail)
            longest_tail = find_longest_tail(peer.taillist)
            logger.debug(f"{env.now} P{peer.id} mines B{block.id}")
            # update peer balance and forward the block
            peer.balance += 50
            env.process(forward_block(block, peer, peer, env))

# generate random graph
peers, links = generate_random_graph(n_peers, z0_slow, z1_low)
RANDOM_SEED = int(time.time())
SIM_TIME = 600

random.seed(RANDOM_SEED)
env = simpy.Environment()

# start with the genesis block in all peers
genesis = Block()
genesis.id = 1
genesis_node = TreeNode(genesis, None)
for i in range(n_peers):
    peers[i].tree = genesis_node
    peers[i].blockids.append(genesis.id)
    peers[i].taillist[genesis_node] = 0

# create, forward and receive transactions
for i in range(int(SIM_TIME//I_txn)):
    env.process(handle_transaction(env))

# create, forward and receive blocks
for i in range(n_peers):
    env.process(mine_block(peers[i], env))

env.run(until=SIM_TIME)

# visualize trees for any 5 peers
peerids=[]
for i in range(n_peers):
    peerids.append(i)
#print (peerids)
showpeers = random.sample(peerids, 5)
#print(showpeers)
for peer in showpeers:
    visualize_graph(peers[peer].blockchain, peer)
    print(f"Number of blocks in peer {peer} 's blockchain: ", len(peers[peer].blockids))



# run subprocess bash
subprocess.run(["bash", "extractlog.sh", str(n_peers)])