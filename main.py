import random
import json
import matplotlib.pyplot as plt
import argparse

class Checker:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.vote = None
        #self.trustworthiness = 1
        self.trustworthiness = {}
        self.wrong_votes = 0
        self.deposit = 1000
        self.balance = 0
        
def everyone_votes(cat):
    for checker in checkers:
        if cat not in checker.trustworthiness:
            checker.trustworthiness[cat] = 1
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
        

def consensus(cat):
    sum_of_weights = sum([checker.trustworthiness[cat] for checker in checkers])
    true_votes = 0
    voters_count = 0
    total_votes = 0
    for checker in checkers:
        if checker.vote:
            total_votes += checker.trustworthiness[cat]
            true_votes += 1
        voters_count += 1
    return total_votes > sum_of_weights/2

def update_trustworthiness(timer, consensus_res, cat):
    for checker in checkers:
        if checker.vote != consensus_res:
            # checker.trustworthiness = max(0, checker.trustworthiness - PENALTY)
            checker.wrong_votes += 1
            # checker.trustworthiness = max(0, checker.trustworthiness - (checker.trustworthiness-0.8)**2*.01 - 0.001*checker.wrong_votes)
            checker.trustworthiness[cat] = max(0, checker.trustworthiness[cat] - (checker.trustworthiness[cat] - (1-checker.wrong_votes/(timer+1)))**2*.1 )
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

def plot_graph(cat):
    plt.plot(mal[cat], 'r-', label='malicious')
    plt.plot(sh[cat], 'g-', label='strong_honest')
    plt.plot(wh[cat], 'b-', label='weak_honest')
    plt.xlabel('Timer')
    plt.ylabel('Trustworthiness')
    plt.title(f'Trustworthiness for {cat}')
    plt.legend()
    plt.show()  

n_malicious = int(q*N)
n_strong_honest = int(p*(N-n_malicious))
n_weak_honest = N - n_malicious - n_strong_honest


malicious = [i for i in range(n_malicious)]
strong_honest = [i for i in range(n_malicious, n_malicious+n_strong_honest)]
weak_honest = [i for i in range(n_malicious+n_strong_honest, N)]
# ideal trustworthiness malicious:0, strong_honest:0.9, weak_honest:0.7
checkers = []
for i in range(N):
    checkers.append(Checker(i, 'malicious') if i in malicious else Checker(i, 'strong_honest') if i in strong_honest else Checker(i, 'weak_honest'))

wrong = 0
wrong_index = []
ITEMS = json.load(open('news.json', 'r'))
NITEMS = len(ITEMS)

mal={}
sh={}
wh={}
cat_all = set()
for i in range(len(ITEMS)):
    is_real = ITEMS[i]['is_real']
    cat = ITEMS[i]['cat']
    cat_all.add(cat)
    everyone_votes(cat)
    consensus_current = consensus(cat)
    if consensus_current != is_real:
        wrong += 1
        wrong_index.append(i)

    update_trustworthiness(i, consensus_current, cat)
    if cat not in mal:
        mal[cat] = []
        sh[cat] = []
        wh[cat] = []
    else:
        if len(malicious) > 0:
            mal[cat].append(checkers[malicious[0]].trustworthiness[cat])
        if len(strong_honest) > 0:
            sh[cat].append(checkers[strong_honest[0]].trustworthiness[cat])
        if len(weak_honest) > 0:
            wh[cat].append(checkers[weak_honest[0]].trustworthiness[cat])

for cat in cat_all:     
    plot_graph(cat)


for checker in checkers:
    print(f"CHECKER {checker.id+1}", end="\t")
    for cat in cat_all:
        print(f"TRUST_{cat} {format(checker.trustworthiness[cat], '.2f')}", end="\t")
    print(f"BALANCE {checker.balance}\tDEPOSIT {format(checker.deposit, '.0f')}\tTYPE {checker.type}")


print(f"\nnumber of wrong consensus  : {wrong}  ")
print(f"\nwrong consensus news items : {wrong_index}")
print()
