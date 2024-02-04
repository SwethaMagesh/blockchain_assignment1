import random
from helper import *

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