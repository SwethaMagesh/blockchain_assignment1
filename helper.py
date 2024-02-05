import random

def exponential_sample(mean):
    return random.expovariate(1 / mean)

def uniform_sample(low, high):
    return random.uniform(low, high)
# def generate_Tk(peer, interval = 600):
#         mean = interval / peer.hashpower
#         Tk = random.expovariate(1 / mean)
#         return Tk
