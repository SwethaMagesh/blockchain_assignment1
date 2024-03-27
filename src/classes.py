'''
This file has 5 classes: Peer, Link, Block, Transaction, TreeNode
Main functionality of each class is as follows:
    Peer: 
        - It is a node in the network
        - It has a list of transactions (mempool), and a blockchain
        - It can add a block to its blockchain
        - It can print the whole blockchain
        - It can return the length of the longest chain
        - It can return the longest chain
    Selfish Peer (Inherits from Peer):
        - It is a node in the network (adv 1 or adv 2)
        - It has a list of transactions (mempool), a blockchain, and a private chain
        - It overrides functions of Peer class - form block, add to private chain, release from private chain, discard private chain
    Link:
        - It is an edge in the network
        - It has a delay value stored
    Block:
        - It is a block in the blockchain
        - It has a list of transactions
        - It can form a block
        - It can generate block delay for a given link based on latency calculations
    Transaction:
        - It is a transaction in the network which has a payer, payee, and coins
        - It can generate a delay for a given link
    TreeNode:
        - It is a node in the blockchain & has a block and a prevNode
        - It can print the whole blockchain
        - It can return the length of the chain

'''

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

    def form_block(self, prevblockid):
        Block.id += 1
        block = Block()
        block.id = Block.id
        MAXTRANSACTIONS = 10
        no_of_txn = random.randint(1, MAXTRANSACTIONS)
        transactions = self.transactions_queue[0:no_of_txn]
        transactions = list(filter(lambda txn: txn.payer.balance >= txn.coins, transactions))
        block.transactions = transactions
        self.transactions_queue = self.transactions_queue[no_of_txn:]
        block.prevblockid = prevblockid
        block.coinbase = Transaction(None, self, 50)
        return block
    
    def __str__(self):
        return str(self.id) + " " + str(self.is_slow) + " " + str(self.is_lowcpu) + " " + str(self.hashpower)

    def add_block_to_tail(self, block, tail_node):
        self.blockchain.add_node(block.id)
        self.blockchain.add_edge(block.id, tail_node.block.id)
        node = TreeNode(block, tail_node)
        self.taillist[node] = self.taillist[tail_node] + 1
        del self.taillist[tail_node]
        longest_tail = find_longest_tail(self.taillist)
        self.blockids.append(block.id)
        self.add_pending_blocks(node)
        if longest_tail == node:
            for txn in block.transactions:
                if txn in self.transactions_queue:
                    self.transactions_queue.remove(txn)
            return True
        else:
            return False

    def add_pending_blocks(self, node):
        for block in self.pending_blocks_queue:
            if block.prevblockid == node.block.id and node in self.taillist:
                # Adding pending block {block.id} to tail of peer P{self.id}
                self.pending_blocks_queue.remove(block)
                self.add_block_to_tail(block, node)
            

    def add_block_to_nontail(self, block, prev_node):
        self.blockchain.add_node(block.id)
        self.blockchain.add_edge(block.id, prev_node.block.id)
        node = TreeNode(block, prev_node)
        self.taillist[node] = prev_node.count_tree() + 1
        self.blockids.append(block.id)
        self.add_pending_blocks(node)

    def print_whole_tree(self):
        print(f"Peer {self.id} Whole Tree => ", end=" ")
        for node in self.taillist:
            node.print_tree(self)

    def longest_chain_length(self):
        longest_tail = find_longest_tail(self.taillist)
        return self.taillist[longest_tail]

    def longest_chain(self):
        longest_tail = find_longest_tail(self.taillist)
        node = longest_tail
        list = []
        while node.prevNode != None:
            list.append(node.block.id)
            node = node.prevNode
        list.append(node.block.id)
        return list
    
    def visualize_graph(self, G, figure_no):
        colors = ['pink' if node in self.created_blocks else 'skyblue' for node in G.nodes()]
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=150, node_color=colors, font_size=8,
                font_color="black", font_weight="bold", edge_color="gray", linewidths=0.5)
        plt.savefig(f'../figs/fig{figure_no}.png')
        plt.clf()

class SelfishPeer(Peer):
    def __init__(self, peer, slow, lowcpu, hashpower):
        super().__init__(peer, slow, lowcpu, hashpower)
        self.is_selfish = True
        self.private_chain = []
        self.is_zero_dash_state = False

    def form_block(self, blockid):
        Block.id += 1
        block = Block()
        block.id = Block.id
        MAXTRANSACTIONS = 10
        no_of_txn = random.randint(1, MAXTRANSACTIONS)
        transactions = self.transactions_queue[0:no_of_txn]
        transactions = list(filter(lambda txn: txn.payer.balance >= txn.coins, transactions))
        block.transactions = transactions
        self.transactions_queue = self.transactions_queue[no_of_txn:]
        if len(self.private_chain) == 0:
            block.prevblockid = blockid
        else:
            block.prevblockid = self.private_chain[-1].id
        block.coinbase = Transaction(None, self, 50)
        return block
    
    def add_to_private_chain(self, block):
        self.private_chain.append(block)
    
    def longest_chain_length_visible(self):
        max_len  = 0
        for tail in self.taillist:
            if tail.block not in self.private_chain:
                if self.taillist[tail] > max_len:
                    max_len = self.taillist[tail]
        return max_len
    

    def release_blocks(self, num):
        to_release =  self.private_chain[:num]
        self.private_chain = self.private_chain[num:]
        return to_release
    
    def discard_private(self):
        self.private_chain = []

    def visualize_graph(self, G, figure_no):
        colors = []
        ids = [block.id for block in  self.private_chain]
        for node in G.nodes():
            if node in ids:
                colors.append('red')
            elif node in self.created_blocks:
                colors.append('pink')
            else:
                colors.append('skyblue')
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=150, node_color=colors, font_size=8,
                font_color="black", font_weight="bold", edge_color="gray", linewidths=0.5)
        plt.savefig(f'../figs/fig{figure_no}.png')
        plt.clf()


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


    def generate_qdelay(self, link):
        n = len(self.transactions)+1
        # 1KB / c Mbps => since message is in bits factor of 8 steps in
        # after simplification, 8/(cij*1024) is the factor
        m_by_cij = n*8/(link.cij*1024)
        # milliseconds to seconds
        roij = link.roij/1000
        # mean = 96 / (cij * 1024) => 96Kbps / cij Mbps
        mean = 96 / (link.cij * 1024)
        dij = exponential_sample(mean)
        return (roij + dij + m_by_cij)


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
        # 1KB / c Mbps => since message is in bits factor of 8 steps in
        # after simplification, 8/(cij*1024) is the factor
        m_by_cij = 8/(link.cij*1024)
        # milliseconds to seconds
        roij = link.roij/1000
        # mean = 96 / (cij * 1024) => 96Kbps / cij Mbps
        mean = 96 / (link.cij * 1024)
        dij = exponential_sample(mean)
        return (roij + dij + m_by_cij)

    def __str__(self) -> str:
        if self.payer == None:
            return f"T{self.id}: P{self.payee.id} mines {self.coins} coins"
        return f"T{self.id}: P{self.payer.id} pays P{self.payee.id} {self.coins} coins"


class TreeNode:
    def __init__(self, block, prev):
        self.block = block
        self.prevNode = prev

    def __str__(self):
        return str(self.block.id)

    def print_tree(self, peer):
        node = self
        print(f"Peer {peer.id} Tree => ", end=" ")
        while node.prevNode != None:
            print(node.block.id, end=" <- ")
            node = node.prevNode
        print(node.block.id)

    def count_tree(self):
        c = 0
        node = self
        while node.prevNode != None:
            node = node.prevNode
            c += 1
        return c