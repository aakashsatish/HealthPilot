from redis import Redis
from rq import Queue
from .jobs import test_job, process_upload_job, process_lab_report_job

# Redis connection
redis_conn = Redis(host='localhost', port=6379, db=0)

# Create queue
default_queue = Queue('default', connection=redis_conn)

def enqueue_test_job(name="World"):
    """Enqueue a test job"""
    job = default_queue.enqueue(test_job, name)
    return {"job_id": job.id, "status": "queued"}

def enqueue_upload_job(file_path: str):
    """Enqueue a file processing job"""
    job = default_queue.enqueue(process_upload_job, file_path)
    return {"job_id": job.id, "status": "queued"}

def enqueue_lab_report_job(file_path: str, report_id: str):
    """Enqueue a lab report processing job"""
    job = default_queue.enqueue(process_lab_report_job, file_path, report_id)
    return {"job_id": job.id, "status": "queued"}