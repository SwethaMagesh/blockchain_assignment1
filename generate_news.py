import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--items', type=int, default=50)
args = parser.parse_args()
ITEMS = args.items
NITEMS = []
for i in range(ITEMS):
    cat_rand = random.choices(['Finance', 'Technology', 'Fashion'])[0]
    news_dict = {"id":i, "cat":cat_rand, "is_real": random.choices([True, False])[0]}
    NITEMS.append(news_dict)

import json
with open('news.json', 'w') as f:
    json.dump(NITEMS, f)