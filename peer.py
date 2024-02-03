class Peer:
    # id
    # links
    # hashingpower
    # slow/not
    # slowcpu/not
    # tree

    def __init__(self, i, slow, slowcpu, hashingpower):
        self.id = i
        self.slow = slow
        self.slowcpu = slowcpu
        self.hashpower = hashingpower
    
    def __str__(self):
        return str(self.id) + " " + str(self.slow) + " " + str(self.slowcpu)+ " " + str(self.hashpower)
    

    



class Link:
    # latency cij
    # ro ij
    def __init__(self, i, j, cij, roij):
        self.i = i
        self.j = j
        self.cij = cij
        self.roij = roij

    def __str__(self):
        return str(self.i) + " " + str(self.j) + " " + str(self.cij) + " " + str(self.roij)
    
    
    
        

