import random

class Transaction:
    txn_id = 0
    def __init__(self, sender, receiver, coins): 
        txn_id += 1
        self.txnid = txn_id
        self.sender = sender
        self.receiver = receiver
        self.coins = coins

    def __init__(self, miner):
        txn_id += 1
        self.txnid = txn_id
        self.sender = None
        self.coins = 50
        self.receiver = miner

    def generate_qdelay(self, link):
        cij = link.cij
        mean = 96 / (cij * 1024) # 96 kb and cij Mbps gives mean in seconds
        dij = random.expovariate(1 / mean)
        return dij