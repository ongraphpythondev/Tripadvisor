
import csv
from tasks import add_to_queue
    

if __name__ == "__main__":
    procs = []
    with open('accounts.csv') as f:
        linesObj = csv.reader(f)

        # Instantiating multiple process with arguments
        count=0
        for row in linesObj:
           count+=1
           print("task added to queue",count)
           add_to_queue.delay(row)