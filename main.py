import random
import json
class Checker:
    def __init__(self, id, type, trustworthiness):
        self.id = id
        self.type = type
        self.vote = None
        self.trustworthiness = 1
        
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
    print(f"TOTAL VOTES {total_votes} SUM OF WEIGHTS {sum_of_weights}")
    return total_votes > sum_of_weights/2

def update_trustworthiness():
    for checker in checkers:
        if checker.vote != is_real:
            checker.trustworthiness = max(0, checker.trustworthiness - PENALTY)
    


N = 10
q = 0.3
p = 0.5

PENALTY = 1/500

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
for i in range(len(ITEMS)):
    is_real = ITEMS[i]['is_real']
    cat = ITEMS[i]['cat']
    everyone_votes()
    consensus_current = consensus()
    if consensus_current != is_real:
        wrong += 1
        wrong_index.append(i)
    update_trustworthiness()
    

print(f"WRONG: {wrong}  ")
for checker in checkers:
    print(f"CHECKER {checker.id} TYPE {checker.type} TRUSTWORTHINESS {round(checker.trustworthiness,2)}")

print(f"WRONG INDICES {wrong_index}")


