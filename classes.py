import random
from helper import *

class Peer:
    def __init__(self, peer, slow, lowcpu, hashpower):
        self.id = peer
        self.is_slow = slow
        self.is_lowcpu = lowcpu
        self.hashpower = hashpower
        self.transactions_queue = []
        self.blockids = []
        self.taillist = {}
        self.pending_blocks_queue = []
        self.balance = 0
        self.blockchain = nx.Graph()
        self.created_blocks = []
    
    def __str__(self):
        return str(self.id) + " " + str(self.is_slow) + " " + str(self.is_lowcpu)+ " " + str(self.hashpower)
    
    def add_block_to_tail(self, block, tail_node):
        self.blockchain.add_node(block.id)
        self.blockchain.add_edge(block.id, tail_node.block.id)
        self.blockids.append(block.id)
        node = TreeNode(block, tail_node)
        self.taillist[node] = self.taillist[tail_node] + 1
        del self.taillist[tail_node]
        longest_tail =  find_longest_tail(self.taillist)
        if longest_tail == node:
            for txn in block.transactions:
                if txn in self.transactions_queue:
                    self.transactions_queue.remove(txn)
            return True
        else:
            return False
    
    def add_block_to_nontail(self, block, prev_node):
        self.blockchain.add_node(block.id)
        self.blockchain.add_edge(block.id, prev_node.block.id)
        self.blockids.append(block.id)
        node = TreeNode(block, prev_node)
        self.taillist[node] = prev_node.count_tree() + 1
        # print("FORKED ",end=" ")
        # node.print_tree(self)
        longest_tail =  find_longest_tail(self.taillist)
        # print("LONGEST TAIL ",end=" ")
        # longest_tail.print_tree(self)

    def print_whole_tree(self):
        print(f"Peer {self.id} Whole Tree => ", end=" ")
        for node in self.taillist:
            node.print_tree(self)

    def longest_chain_length(self):
        longest_tail = find_longest_tail(self.taillist)
        return longest_tail.count_tree()
    
    def longest_chain(self):
        longest_tail = find_longest_tail(self.taillist)
        node = longest_tail
        list = []
        while node.prevNode != None:
            list.append(node.block.id)
            node = node.prevNode
        list.append(node.block.id)
        return list

class Link:
    def __init__(self, i, j, cij, roij):
        self.i = i
        self.j = j
        self.cij = cij
        self.roij = roij

    def __str__(self):
        return str(self.i) + " " + str(self.j) + " " + str(self.cij) + " " + str(self.roij)
    
class Block:
    id = 1
    def __init__(self): 
        self.sent_peers = set()
        
    def form_block(self, peer):
        # if len(peer.transactions_queue) == 0:
            # print(f"Peer {peer.id} creating empty block")
            # return False
        Block.id += 1
        self.id = Block.id
        no_of_txn = random.randint(1, 10)
        transactions = peer.transactions_queue[0:no_of_txn]
        transactions = list(filter(lambda txn: txn.payer.balance >= txn.coins, transactions))
        self.transactions = transactions
        peer.transactions_queue = peer.transactions_queue[no_of_txn:]
        tail_node = find_longest_tail(peer.taillist)
        self.prevblockid = tail_node.block.id
        self.coinbase = Transaction(None, peer, 50)
        return True

    def generate_qdelay(self, link):
        n = len(self.transactions)+1
        m_by_cij = n*8/(link.cij*1024)
        roij = link.roij/1000
        mean = 96 / (link.cij * 1024)
        dij = exponential_sample(mean)
        return (roij +  dij + m_by_cij)
    
class Transaction:
    txn_id = 0
    def __init__(self, payer, payee, coins): 
        Transaction.txn_id += 1
        self.id = Transaction.txn_id
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
    
    def __str__(self) -> str:
        return f"Txn {self.id} {self.payer.id} -> {self.payee.id} {self.coins}"
    

class TreeNode:
# simulate a Tree in a blockchain p2p network
    def __init__(self, block, prev):
        self.block = block
        self.prevNode = prev
    
    def __str__(self):
        return str(self.block.id)
    
    def print_tree(self, peer):
        c = 1
        node = self
        print(f"P{peer.id} => ", end=" ")
        while node.prevNode != None:
            print(node.block.id, end=" <- ")
            c+=1
            node = node.prevNode
        c+=1
        print(node.block.id, " L= ",c)
        return c
    
    def count_tree(self):
        c = 0 
        node = self
        while node.prevNode != None:
            node = node.prevNode
            c+=1
        return c

    

    

