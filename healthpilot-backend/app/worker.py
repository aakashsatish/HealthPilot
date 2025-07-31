import os
from rq import Worker, Queue
from redis import Redis

# Redis connection
redis_conn = Redis(host='localhost', port=6379, db=0)

# Create queues
default_queue = Queue('default', connection=redis_conn)
high_queue = Queue('high', connection=redis_conn)

def start_worker():
    """Start RQ worker"""
    worker = Worker([default_queue, high_queue], connection=redis_conn)
    worker.work()

if __name__ == '__main__':
    start_worker()