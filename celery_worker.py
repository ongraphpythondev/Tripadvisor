import os

if __name__ == "__main__":
    # os.system("celery -A tasks worker --loglevel=INFO --concurrency=15 -n worker1 -l info -P gevent")

    os.system("celery -A tasks worker --loglevel=INFO --concurrency=2 -n worker1 -l info -P gevent")