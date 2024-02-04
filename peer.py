from blockchain import *
from main import *

class Peer:
    def __init__(self, peer, slow, lowcpu, hashpower):
        self.id = peer
        self.slow = slow
        self.slowcpu = lowcpu
        self.hashpower = hashpower
        self.transactions_queue = []
    
    def __str__(self):
        return str(self.id) + " " + str(self.slow) + " " + str(self.slowcpu)+ " " + str(self.hashpower)
    
    def forward_transaction(self, transaction, sender_peer, env):
        # all adjacent peers except sender
        for adj in G.adj[self.id]:
            if adj != sender_peer.id:
                # send transaction to adj peer
                peers[adj].forward_transaction(transaction, self, env)
                yield env.timeout(transaction.generate_qdelay(links[self.id][adj]))
                pass





    def receive_transaction(self, transaction):
        trans_ids = [x.id for x in self.transactions_queue]
        if transaction not in trans_ids:
            self.transactions_queue.append(transaction)

class Link:
    def __init__(self, i, j, cij, roij):
        self.i = i
        self.j = j
        self.cij = cij
        self.roij = roij

    def __str__(self):
        return str(self.i) + " " + str(self.j) + " " + str(self.cij) + " " + str(self.roij)