import random
import json
import matplotlib.pyplot as plt
import argparse

class Checker:
    def __init__(self, id, type, trustworthiness):
        self.id = id
        self.type = type
        self.vote = None
        self.trustworthiness = 1
        self.wrong_votes = 0
        self.deposit = 1000
        self.balance = 0
        
def everyone_votes():
    for checker in checkers:
        if checker.type == 'malicious':
            # other attack
            # if random.random() < 0.5:
            #     checker.vote = True
            # else:
            #     checker.vote = False
            checker.vote = not is_real
        elif checker.type == 'strong_honest':
            checker.vote = is_real if random.random() < 0.9 else not is_real
        elif checker.type == 'weak_honest':
            checker.vote = is_real if random.random() < 0.7 else not is_real
        

def consensus():
    sum_of_weights = sum([checker.trustworthiness for checker in checkers])
    true_votes = 0
    voters_count = 0
    total_votes = 0
    for checker in checkers:
        if checker.vote:
            total_votes += checker.trustworthiness
            true_votes += 1
        voters_count += 1
    return total_votes > sum_of_weights/2

def update_trustworthiness(timer, consensus_res):
    for checker in checkers:
        if checker.vote != consensus_res:
            # checker.trustworthiness = max(0, checker.trustworthiness - PENALTY)
            checker.wrong_votes += 1
            # checker.trustworthiness = max(0, checker.trustworthiness - (checker.trustworthiness-0.8)**2*.01 - 0.001*checker.wrong_votes)
            checker.trustworthiness = max (0,
             checker.trustworthiness - (checker.trustworthiness - (1-checker.wrong_votes/(timer+1)))**2 *0.1
            )
            checker.deposit -= 1
        else:
            checker.balance += 1
        
            
parser = argparse.ArgumentParser()
parser.add_argument('-N', type=int, default=50)
parser.add_argument('-q', type=float, default=0.4)
parser.add_argument('-p', type=float, default=0.5)
args = parser.parse_args()
N = args.N
q = args.q
p = args.p


n_malicious = int(q*N)
n_strong_honest = int(p*(N-n_malicious))
n_weak_honest = N - n_malicious - n_strong_honest


malicious = [i for i in range(n_malicious)]
strong_honest = [i for i in range(n_malicious, n_malicious+n_strong_honest)]
weak_honest = [i for i in range(n_malicious+n_strong_honest, N)]
# ideal trustworthiness malicious:0, strong_honest:0.9, weak_honest:0.7
checkers = []
for i in range(N):
    checkers.append(Checker(i, 'malicious', 1) if i in malicious else Checker(i, 'strong_honest', 1) if i in strong_honest else Checker(i, 'weak_honest', 1))

wrong = 0
wrong_index = []
ITEMS = json.load(open('news.json', 'r'))
NITEMS = len(ITEMS)
# plot trustworthiness vs time
mal=[]
sh=[]
wh=[]
for i in range(len(ITEMS)):
    is_real = ITEMS[i]['is_real']
    cat = ITEMS[i]['cat']
    everyone_votes()
    consensus_current = consensus()
    if consensus_current != is_real:
        wrong += 1
        wrong_index.append(i)
    update_trustworthiness(i, consensus_current)
    if len(malicious) > 0:
        mal.append(checkers[malicious[0]].trustworthiness)
    if len(strong_honest) > 0:
        sh.append(checkers[strong_honest[0]].trustworthiness)
    if len(weak_honest) > 0:
        wh.append(checkers[weak_honest[0]].trustworthiness)
       
#  plot mal, sh, wh
plt.plot(mal, label='malicious')
plt.plot(sh, label='strong_honest')
plt.plot(wh, label='weak_honest')
plt.legend()
plt.xlabel('News items')
plt.ylabel('Trustworthiness')
plt.title('Trustworthiness vs Time')
# plt.show()
plt.savefig('trustworthiness_vs_time.png')


# format printing


print(f"N={N}, p={p}, q={q}, NITEMS={NITEMS}")
print(f"MALICIOUS {len(malicious)}, STRONG_HONEST {len(strong_honest)}, WEAK_HONEST {len(weak_honest)}")
print(f"Wrong={wrong}")
# check if list has entries : [checkers[malicious[0]], checkers[strong_honest[0]], checkers[weak_honest[0]]]
if len(malicious) > 0:
    print(f"Malicious       checker  {checkers[malicious[0]].id} trustworthiness {round(checkers[malicious[0]].trustworthiness,2)}, balance {checkers[malicious[0]].balance}, deposit {checkers[malicious[0]].deposit}")
if len(strong_honest) > 0:
    print(f"Strong honest   checker {checkers[strong_honest[0]].id} trustworthiness {round(checkers[strong_honest[0]].trustworthiness,2)}, balance {checkers[strong_honest[0]].balance}, deposit {checkers[strong_honest[0]].deposit}")
if len(weak_honest) > 0:
    print(f"Weak honest     checker {checkers[weak_honest[0]].id} trustworthiness {round(checkers[weak_honest[0]].trustworthiness,2)}, balance {checkers[weak_honest[0]].balance}, deposit {checkers[weak_honest[0]].deposit}")



