from celery import Celery
from main import main
import os, sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath)

BROKER_URL = "redis://localhost:6379/1"
app = Celery("tasks", broker=BROKER_URL)

@app.task
def add_to_queue(row):
    main(row)
