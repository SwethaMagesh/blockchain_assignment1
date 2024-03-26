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
logging.basicConfig(filename="../logs/blockchain.log",
                    format='%(message)s', filemode='w')
logger = logging.getLogger('main.py')
logger.setLevel(logging.DEBUG)

# Courtesy: https://docs.python.org/3/library/argparse.html
# parse command line arguments n, z0, z1, Ttx, I
parser = argparse.ArgumentParser(description="command line argument parser")
# number of peers in the network
parser.add_argument("--peers", "-n", type=int, default=10,
                    required=True, help="enter the number of peers in the network")
#  inter arrival time of transactions
parser.add_argument("--txninterval", "-Ttx", type=float, default=5,
                    required=True, help="enter the inter arrival time of transactions")
#  inter arrival time of blocks
parser.add_argument("--blockinterval", "-I", type=float, default=10,
                    required=True, help="enter the inter arrival time of blocks")
#  hashing power of selfish miner 1
parser.add_argument("--zeta1", "-a1", type=float, default=10,
                    required=True, help="enter the hashing power of selfish miner 1")
#  hashing power of selfish miner 2
parser.add_argument("--zeta2", "-a2", type=float, default=10,
                    required=True, help="enter the hashing power of selfish miner 1")

args = parser.parse_args()
n_peers = args.peers
z0_slow = 0.5
I_txn = args.txninterval
I_block = args.blockinterval
zeta1 = args.zeta1
zeta2 = args.zeta2

# local printing
print("peers in network        = ", n_peers)
print("transaction interval    = ", I_txn)
print("block interval          = ", I_block)
print('attacker1 hpower        = ',zeta1)
print('attacker2 hpower        = ',zeta2)

# Constants
TRANSACTION_SIZE = 1  # in KB
MAX_BLOCK_SIZE = 1024  # in KB
START_TIME = 0

# generate a random graph with n peers and parameters
G = nx.Graph()
figure_no = 0


def generate_random_graph(n_peers, z0_slow):
    # add all peers as nodes
    for peer in range(n_peers):
        G.add_node(peer)
    # add edges b/w random nodes with degrees in {3...6}
    for node in G.nodes():
        degree = random.randint(3, 6)
        while G.degree(node) < degree:
            possible_nodes = [other_node for other_node in G.nodes(
            ) if other_node != node and G.degree(other_node) < 6]
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

    # randomly allocate nodes as slow 
    slow_peers = random.sample(range(2, n_peers), int(z0_slow * (n_peers-2)))

    # calculate hashpower of slow and fast nodes
    hashpower = (1-zeta1-zeta2) / (n_peers - 2)

    # populate peers with their parameters
    peers = []
    peers.append(SelfishPeer(0, slow=False, lowcpu=False, hashpower=zeta1))
    peers.append(SelfishPeer(1, slow=False, lowcpu=False, hashpower=zeta2))
    for peer in range(2, n_peers):
        if peer in slow_peers:
            is_slow = True
        else:
            is_slow = False
        is_lowcpu = True
        peers.append(
            Peer(peer, slow=is_slow, lowcpu=is_lowcpu, hashpower=hashpower))

    # populate links with their parameters
    links = {}
    for i, j in G.edges():
        ro = uniform_sample(10, 500)
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
    s, r, c = create_random_transaction(n_peers, peers)
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
                receive_transaction(
                    peers[neighbour], curr_peer, transaction, env)
                env.process(forward_transaction(
                    transaction, peers[neighbour], curr_peer, env))

# forward blocks similar to transactions


def forward_block(block, curr_peer, prev_peer, env):
    if curr_peer.id in block.sent_peers:
        return
    if is_selfish(curr_peer) and not is_selfish(prev_peer):
        logger.debug(f"{env.now} P{curr_peer.id} does not forward B{block.id}")
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
                env.process(forward_block(
                    block, peers[neighbour], curr_peer, env))

# receive block from peers


def receive_block(peer, hears_from, block, env):
    logger.debug(
        f"{env.now} P{peer.id} recvs B{block.id} from P{hears_from.id}")
    # if block is not already processed, validate it
    if is_selfish(peer):
        # calculate visible length before adding
        visible_len = peer.longest_chain_length_visible()
    if block.id not in peer.blockids:
        isvalid = validate_block(block)
        chainlen_changed = False
        if isvalid:
            # add to tree if parent block is found
            if block.prevblockid in peer.blockids:
                chainlen_changed = traverse_and_add(peer, block)
                logger.debug(
                    f"{env.now} P{peer.id} adds B{block.id} to its tree")
            # add to pending queue if parent block is not found
            else:
                logger.debug(
                    f"{env.now} P{peer.id} adds B{block.id} to its pending queue")
                peer.pending_blocks_queue.append(block)
            # start mining a new block if current block is added to the longest chain
            if chainlen_changed:
                env.process(mine_block(peer, env))
        else:
            logger.debug(f"{env.now} P{peer.id} rejects invalid B{block.id}")
        if is_selfish(peer):
            # visible leng changed
            new_vis_length = peer.longest_chain_length_visible()
            if new_vis_length > visible_len:
                lead = len(peer.private_chain)
                # what should the selfish guy do?
                if lead == 1:
                    peer.is_zero_dash_state = True
                else:
                    peer.is_zero_dash_state = False
                if lead in [1, 2]:
                    # release all private blocks
                    released_blocks = peer.release_blocks(lead)
                    peer.balance += 50*lead
                    for block in released_blocks:
                        logger.debug(f"{env.now} P{peer.id} makes B{block.id} public")
                        env.process(forward_block(block, peer, peer, env))

                elif lead > 2:
                    released_blocks = peer.release_blocks(1)
                    peer.balance += 50
                    logger.debug(f"{env.now} P{peer.id} makes B{released_blocks[0].id} public")
                    # release 1 block
                    env.process(forward_block(released_blocks[0], peer, peer, env))
                else:
                    # mine on new longest
                    peer.discard_private()
    

# mining process of a new block
def mine_block(peer, env):
    if is_selfish(peer):
        longest_tail = find_longest_tail(peer.taillist)
        mining_time = generate_Tk(peer, I_block)
        # start mining
        logger.debug(
            f"{env.now} P{peer.id} selfishly mines for {mining_time} seconds")
        logger.debug(
            f"{env.now} P{peer.id} private chain length = {len(peer.private_chain)}")
        yield env.timeout(mining_time)
        longest_tail_new = find_longest_tail(peer.taillist)
        if longest_tail_new == longest_tail:
            block = peer.form_block(longest_tail.block.id)  
            peer.created_blocks += [block.id]
            logger.debug(f"{env.now} P{peer.id} selfishly mines B{block.id} on B{longest_tail.block.id}")
            if not peer.is_zero_dash_state:
                peer.add_to_private_chain(block)
                logger.debug(f"{env.now} P{peer.id} adds B{block.id} to its private chain")
            else:
                env.process(forward_block(block, peer, peer, env))
                logger.debug(f"{env.now} P{peer.id} makes B{block.id} public")
            traverse_and_add(peer, block)
        env.process(mine_block(peer, env))

    else:
        longest_tail = find_longest_tail(peer.taillist)
        mining_time = generate_Tk(peer, I_block)
        # start mining
        logger.debug(f"{env.now} P{peer.id} mines for {mining_time} seconds")
        yield env.timeout(mining_time)
        # stop mining and find the current longest chain
        longest_tail_new = find_longest_tail(peer.taillist)
        # if the longest chain is the same, create a new block
        if longest_tail_new == longest_tail:
            prevblockid = longest_tail.block.id
            block = peer.form_block(prevblockid)
            peer.created_blocks += [block.id]
            peer.add_block_to_tail(block, longest_tail)
            longest_tail = find_longest_tail(peer.taillist)
            logger.debug(f"{env.now} P{peer.id} mines B{block.id} on B{prevblockid}")
            # update peer balance and forward the block
            peer.balance += 50
            env.process(forward_block(block, peer, peer, env))


# generate random graph
peers, links = generate_random_graph(n_peers, z0_slow)
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
showpeers = random.sample(range(2,n_peers), 3)
showpeers = [0, 1] + showpeers
# print(showpeers)
for peer in showpeers:
    peers[peer].visualize_graph(peers[peer].blockchain, peer)
    print(f"Number of blocks in peer {peer} 's blockchain: ", len(
        peers[peer].blockids))
    
print('='*100)
print(f"Number of blocks created in all: {sum([len(peers[peer].created_blocks) for peer in range(n_peers)])} created")
print('='*100)
for peer in [0,1]:
    print(f"Number of blocks in peer {peer} 's created blocks: {len(peers[peer].created_blocks)}")
print('='*100)


# choose a honest node and get its longest chain 
honest_peer = showpeers[-1]
longest_chain = peers[honest_peer].longest_chain()
print(f"Length of longest chain of honest peer {honest_peer} is {len(longest_chain)}")
print(f"Longest chain is {longest_chain}")


# run subprocess bash
subprocess.run(["bash", "extractlog.sh", str(n_peers)])