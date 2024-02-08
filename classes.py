import random
from helper import *
class Peer:
    def __init__(self, peer, slow, lowcpu, hashpower):
        self.id = peer
        self.slow = slow
        self.slowcpu = lowcpu
        self.hashpower = hashpower
        self.transactions_queue = []
        self.tree = None
        self.blockids = []
        self.taillist = {}
        self.pending_blocks_queue = []
        self.balance = 0
    
    def __str__(self):
        return str(self.id) + " " + str(self.slow) + " " + str(self.slowcpu)+ " " + str(self.hashpower)
    
    def add_block_to_tail(self, block, tail_node):
        self.blockids.append(block.id)
        node = TreeNode(block, tail_node)
        self.taillist[node] = self.taillist[tail_node] + 1
        del self.taillist[tail_node]
        longest_tail =  max(self.taillist, key=self.taillist.get)
        if longest_tail == node:
            return True
        else:
            return False


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
        self.sent_peers = set()
        
    def form_block(self, peer):
        no_of_txn = random.randint(1, 10)
        self.transactions = peer.transactions_queue[0:no_of_txn]
        peer.transactions_queue = peer.transactions_queue[no_of_txn:]
        tail_node = max(peer.taillist, key=peer.taillist.get)
        self.prevblockid = tail_node.block.id
        self.coinbase = Transaction(None, peer, 50)

    def generate_qdelay(self, link):
        m_by_cij = 8/(link.cij*1024)
        roij = link.roij/1000
        mean = 96 / (link.cij * 1024)
        dij = exponential_sample(mean)
        return (roij +  dij + m_by_cij)
    
class Transaction:
    txn_id = 0
    def __init__(self, payer, payee, coins): 
        Transaction.txn_id += 1
        self.txnid = Transaction.txn_id
        self.payer = payer
        self.payee = payee
        self.coins = coins
        self.sent_peers = set()

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
    
    
    
    def __str__(self):
        return str(self.block.id)
    
    def print_tree(self):
        node = self
        while node.prevNode != None:
            print(node.block.id, end=" <- ")
            node = node.prevNode
        print(node.block.id)
    

