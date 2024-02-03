class Tree:
    # simulate a Tree in a blockchain p2p network
    def __init__(self, root):
        self.root = root
        self.children = []
        self.parent = None
        self.block = None
        self.transactions = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

   
    
