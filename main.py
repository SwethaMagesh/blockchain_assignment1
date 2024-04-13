import random
import json
import matplotlib.pyplot as plt


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

def update_trustworthiness(timer, cat):
    for checker in checkers:
        if checker.vote != is_real:
            # checker.trustworthiness = max(0, checker.trustworthiness - PENALTY)
            checker.wrong_votes += 1
            # checker.trustworthiness = max(0, checker.trustworthiness - (checker.trustworthiness-0.8)**2*.01 - 0.001*checker.wrong_votes)
            checker.trustworthiness[cat] = max(0, checker.trustworthiness[cat] - (checker.trustworthiness[cat] - (1-checker.wrong_votes/(timer+1)))**2*.01 )
            checker.deposit -= 1
        else:
            checker.balance += 1
        
def plot_graph(cat):
    plt.plot(mal[cat], 'r-', label='malicious')
    plt.plot(sh[cat], 'g-', label='strong_honest')
    plt.plot(wh[cat], 'b-', label='weak_honest')
    plt.xlabel('Timer')
    plt.ylabel('Trustworthiness')
    plt.title(f'Trustworthiness for {cat}')
    plt.show()  

N = 50
q = 0.4
p = 0.5

malicious = random.choices(range(N), k=int(q*N))
honest = [i for i in range(N) if i not in malicious]
strong_honest = random.choices(honest, k=int(p*len(honest)))
weak_honest = [i for i in honest if i not in strong_honest] 

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
    update_trustworthiness(i, cat)
    if cat not in mal:
        mal[cat] = []
        sh[cat] = []
        wh[cat] = []
    else:
        mal[cat].append(checkers[malicious[0]].trustworthiness[cat])
        sh[cat].append(checkers[strong_honest[0]].trustworthiness[cat])
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
