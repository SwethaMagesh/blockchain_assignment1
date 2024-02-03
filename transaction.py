# functionality of create transaction, forward transaction, and receive transaction

class Transaction:
    # id
    # sender
    # receiver

    def create_transaction(self, time, size, transaction_id):
        pass
    
    def forward_transaction(self, peer1, peer2):
        pass
        
    def receive_transaction(self, transaction):
        pass

    def generate_qdelay(self, link):
        cij = link.cij
        mean = 96 / (cij * 1024) # 96 kb and cij Mbps gives mean in seconds
        dij = [random.expovariate(1 / mean) for _ in range(1)]
        return dij[0]