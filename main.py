from hash_func import HashFinder
from tqdm import tqdm

hf = HashFinder()
hf.find(sd=17)

# validity check
"""
for i in tqdm(range(100000)):
    o, o2 = hf.find(sd=i, pt=False)
    if not o==o2:
        print("error")
"""