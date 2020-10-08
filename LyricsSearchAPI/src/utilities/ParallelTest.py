import numpy as np
import time
import sys
from datetime import datetime
# Parallelizing using Pool.apply()
import multiprocessing as mp

# Prepare data
np.random.RandomState(100)
arr = np.random.randint(0, 10, size=[200000, 5])
data = arr.tolist()
data[:5]

print(data[:10])
# Solution Without Paralleization

def howmany_within_range(row, minimum, maximum):
    """Returns how many numbers lie within `maximum` and `minimum` in a given `row`"""
    count = 0
    for n in row:
        if minimum <= n <= maximum:
            count = count + 1
    return count

results = []

start = time.perf_counter()

for row in data:
    results.append(howmany_within_range(row, minimum=4, maximum=8))
 
print(results[:100])

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} seconds')



# Step 1: Init multiprocessing.Pool()
pool = mp.Pool(mp.cpu_count())

start = time.perf_counter()

# Step 2: `pool.apply` the `howmany_within_range()`
results = [pool.apply(howmany_within_range, args=(row, 4, 8)) for row in data]
 
# Step 3: Don't forget to close
pool.close()    
 
print(results[:100])

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} seconds')
