class Peer:
    def __init__(self, peer, slow, lowcpu, hashpower):
        self.id = peer
        self.slow = slow
        self.slowcpu = lowcpu
        self.hashpower = hashpower
    
    def __str__(self):
        return str(self.id) + " " + str(self.slow) + " " + str(self.slowcpu)+ " " + str(self.hashpower)
    
class Link:
    def __init__(self, i, j, cij, roij):
        self.i = i
        self.j = j
        self.cij = cij
        self.roij = roij

    def __str__(self):
        return str(self.i) + " " + str(self.j) + " " + str(self.cij) + " " + str(self.roij)