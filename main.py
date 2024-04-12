import random
import json
import matplotlib.pyplot as plt


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
            checker.vote = not is_real
        elif checker.type == 'strong_honest':
            checker.vote = is_real if random.random() < 0.9 else not is_real
        elif checker.type == 'weak_honest':
            checker.vote = is_real if random.random() < 0.7 else not is_real
        

def consensus():
    sum_of_weights = sum([checker.trustworthiness for checker in checkers])
    total_votes = 0
    for checker in checkers:
        if checker.vote:
            total_votes += checker.trustworthiness
    return total_votes > sum_of_weights/2

def update_trustworthiness(timer):
    for checker in checkers:
        if checker.vote != is_real:
            # checker.trustworthiness = max(0, checker.trustworthiness - PENALTY)
            checker.wrong_votes += 1
            # checker.trustworthiness = max(0, checker.trustworthiness - (checker.trustworthiness-0.8)**2*.01 - 0.001*checker.wrong_votes)
            checker.trustworthiness = max(0, checker.trustworthiness - (checker.trustworthiness - (1-checker.wrong_votes/(timer+1)))**2*.1 )
            checker.deposit -= 1
        else:
            checker.balance += 1
            


N = 10
q = 0.3
p = 0.5


malicious = random.choices(range(N), k=int(q*N))
honest = [i for i in range(N) if i not in malicious]
strong_honest = random.choices(honest, k=int(p*len(honest)))
weak_honest = [i for i in honest if i not in strong_honest] 

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
    update_trustworthiness(i)
    mal.append(checkers[malicious[0]].trustworthiness)
    sh.append(checkers[strong_honest[0]].trustworthiness)
    wh.append(checkers[weak_honest[0]].trustworthiness)
    if i==500:
        for checker in checkers:
            print(f"CHECKER {checker.id} TYPE {checker.type} TRUSTWORTHINESS {round(checker.trustworthiness,2)}")
    
#  plot mal, sh, wh
plt.plot(mal, label='malicious')
plt.plot(sh, label='strong_honest')
plt.plot(wh, label='weak_honest')
plt.show()

print(f"No of WRONG consensus: {wrong}  ")
for checker in checkers:
    print(f"CHECKER {checker.id} TYPE {checker.type} TRUSTWORTHINESS {round(checker.trustworthiness,2)}")



