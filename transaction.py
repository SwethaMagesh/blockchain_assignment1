import random

class Transaction:
    txn_id = 0
    def __init__(self, sender, receiver, coins): 
        Transaction.txn_id += 1
        self.txnid = Transaction.txn_id
        self.sender = sender
        self.receiver = receiver
        self.coins = coins

    def generate_qdelay(self, link):
        m_by_cij = 8/(link.cij*1024)
        roij = link.roij/1000
        mean = 96 / (link.cij * 1024) # 96 kb and cij Mbps gives mean in seconds
        dij = random.expovariate(1 / mean)
        # print(roij +  dij + m_by_cij)
        return (roij +  dij + m_by_cij)