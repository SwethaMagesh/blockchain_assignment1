import random
from peer import Peer
from peer import Link
class Block:
    # transactions: list of transactions
    # blockid
    # coinbase
    # parenthash
    # timestamp
    def __init__(self):
        pass
    def mine_block(self, transactions):
        pass
    def forward_block(self, block, peer):
        pass
    def validate_block(self, block):
        pass
    def receive_block(self, block):
        pass
    def generate_qdelay(self, link):
        cij = link.cij
        mean = 96 / (cij * 1024) # 96 kb and cij Mbps gives mean in seconds
        dij = [random.expovariate(1 / mean) for _ in range(1)]
        return dij[0]

