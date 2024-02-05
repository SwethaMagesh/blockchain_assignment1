import random
from helper import *
class Peer:
    def __init__(self, peer, slow, lowcpu, hashpower):
        self.id = peer
        self.slow = slow
        self.slowcpu = lowcpu
        self.hashpower = hashpower
        self.transactions_queue = []
        self.sent_ids = {}
        self.tree = None
        self.blockids = []
        self.taillist = {}
        self.pending_blocks_queue = []
    
    def __str__(self):
        return str(self.id) + " " + str(self.slow) + " " + str(self.slowcpu)+ " " + str(self.hashpower)

class Link:
    def __init__(self, i, j, cij, roij):
        self.i = i
        self.j = j
        self.cij = cij
        self.roij = roij

    def __str__(self):
        return str(self.i) + " " + str(self.j) + " " + str(self.cij) + " " + str(self.roij)
    
class Block:
    id = 0
    def __init__(self): 
        Block.id += 1
        self.id = Block.id
        
    def form_block(self, peer):
        no_of_txn = random.randint(1, 10)
        self.transactions = peer.transactions_queue[0:no_of_txn]
        peer.transactions_queue = peer.transactions_queue[no_of_txn:]
        tail_node = max(peer.taillist, key=peer.taillist.get)
        self.prevblockid = tail_node.block.id
        self.coinbase = Transaction(None, peer, 50)
    
    def forward_block(self, block, peer):
        pass
    def validate_block(self, block):
        pass
    def receive_block(self, block):
        pass
    def generate_qdelay(self, link):
        cij = link.cij
        mean = 96 / (cij * 1024) # 96 kb and cij Mbps gives mean in seconds
        dij = random.expovariate(mean)
        return dij
    
class Transaction:
    txn_id = 0
    reached_peers = set()
    def __init__(self, sender, receiver, coins): 
        Transaction.txn_id += 1
        self.txnid = Transaction.txn_id
        self.sender = sender
        self.receiver = receiver
        self.coins = coins
        Transaction.reached_peers = set()

    def generate_qdelay(self, link):
        m_by_cij = 8/(link.cij*1024)
        roij = link.roij/1000
        mean = 96 / (link.cij * 1024)
        dij = exponential_sample(mean)
        return (roij +  dij + m_by_cij)
    

class TreeNode:
# simulate a Tree in a blockchain p2p network
    def __init__(self, block, prev):
        self.block = block
        self.prevNode = prev
