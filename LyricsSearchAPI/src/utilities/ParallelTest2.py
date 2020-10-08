import time
import multiprocessing
import concurrent.futures

def doSomething(seconds):
    print(f'sleeping {seconds} second')
    time.sleep(seconds)
    print(f'done sleeping..{seconds}')
   
start = time.perf_counter()
 
with concurrent.futures.ProcessPoolExecutor() as executor: 
    secs = [20,3,3,2,1,2,1,5,18,3,4,2,1 ]
    results = executor.map(doSomething, secs) 


finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} seconds')
    
    
    

    
 