import argparse
from blockchain import generate_random_graph

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

# generate random graph
peers, links = generate_random_graph(n_peers, z0_slow, z1_low)