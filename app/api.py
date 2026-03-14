from fastapi import FastAPI
from core.logger import get_logger
from core.database import DatabaseManager

app = FastAPI()
logger = get_logger()
db = DatabaseManager(logger)


# ---------------------------------
# HEALTH CHECK
# ---------------------------------
@app.get("/system/health")
def health():
    return {"status": "healthy"}


# ---------------------------------
# LIST JOBS
# ---------------------------------
@app.get("/jobs")
def list_jobs():
    return db.get_jobs()


# ---------------------------------
# LIST WORKERS
# ---------------------------------
@app.get("/workers")
def list_workers():
    return db.get_workers()


# ---------------------------------
# METRICS
# ---------------------------------
@app.get("/metrics")
def metrics():
    return {
        "job_counts": db.get_job_counts(),
        "queue_depth": db.get_queue_depth(),
        "worker_count": len(db.get_workers())
    }