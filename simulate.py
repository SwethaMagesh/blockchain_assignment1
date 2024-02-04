import simpy
import random
import time


RANDOM_SEED = int(time.time())
SIM_TIME = 20

random.seed(RANDOM_SEED)
env = simpy.Environment()

txn = Transaction(sender=peers[2], receiver=peers[8], coins=0)

env.process(forward_transaction(peers[2], txn, peers[2], env))