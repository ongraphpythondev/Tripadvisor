
import csv
from tasks import add_to_queue
import os
    

if __name__ == "__main__":
    os.system("gnome-terminal -e 'bash -c \"celery -A tasks worker --loglevel=INFO --concurrency=2 -n worker1 -l info -P gevent; exec bash\"'")
    os.system("gnome-terminal -e 'bash -c \"celery -A tasks worker --loglevel=INFO --concurrency=2 -n worker2 -l info -P gevent; exec bash\"'")
    
    procs = []
    with open('accounts.csv') as f:
        linesObj = csv.reader(f)

        # Instantiating multiple process with arguments
        count=0
        for row in linesObj:
           count+=1
           print("task added to queue",count)
           add_to_queue.delay(row)