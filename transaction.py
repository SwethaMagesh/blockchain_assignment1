import random
from helper import *

class Transaction:
    txn_id = 0
    def __init__(self, payer, payee, coins): 
        Transaction.txn_id += 1
        self.txnid = Transaction.txn_id
        self.payer = payer
        self.payee = payee
        self.coins = coins
        self.will_reach_peers = set()

    def generate_qdelay(self, link):
        m_by_cij = 8/(link.cij*1024)
        roij = link.roij/1000
        mean = 96 / (link.cij * 1024)
        dij = exponential_sample(mean)
        return (roij +  dij + m_by_cij)