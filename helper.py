import random

def exponential_sample(mean):
    return random.expovariate(1 / mean)

def uniform_sample(low, high):
    return random.uniform(low, high)

def create_random_transaction(num_of_peers, initial_state = False):
    payer = random.randint(0, num_of_peers - 1)
    payee = random.randint(0, num_of_peers - 1)
    if initial_state:
        coins = random.randint(0,1)
    coins = random.randint(1, 10)
    return payer, payee, coins


# def generate_Tk(peer, interval = 600):
#         mean = interval / peer.hashpower
#         Tk = random.expovariate(1 / mean)
#         return Tk
