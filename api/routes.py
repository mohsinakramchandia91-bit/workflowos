from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from core.logger import get_logger
from core.database import DatabaseManager
from plugins.plugin_manager import PluginManager
from core.config import PLUGINS_PATH

router = APIRouter()

logger = get_logger("api")
db = DatabaseManager(logger)

# FIX: PluginManager requires logger
plugin_manager = PluginManager(PLUGINS_PATH, logger)


# ================= API KEY SECURITY =================

def validate_api_key(x_api_key: str = Header(...)):
    with db._connect() as conn:
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM api_keys WHERE key=%s",
            (x_api_key,)
        )

        if not cur.fetchone():
            raise HTTPException(status_code=403, detail="Invalid API Key")


# ================= JOB CREATE =================

class JobCreate(BaseModel):
    plugin: str
    tenant_id: str = "default"
    priority: int = 5


@router.post("/jobs", dependencies=[Depends(validate_api_key)])
def create_job(job: JobCreate):

    job_id = db.add_job(
        plugin_name=job.plugin,
        tenant_id=job.tenant_id,
        priority=job.priority
    )

    logger.info(f"API created job {job_id}")

    return {"job_id": job_id}


# ================= GET JOB =================

@router.get("/jobs/{job_id}")
def get_job(job_id: int):

    job = db.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


# ================= METRICS =================

@router.get("/metrics")
def metrics():

    return db.get_metrics()


# ================= DEEP HEALTH CHECK =================

@router.get("/health")
def health():

    try:

        # Check database connection
        with db._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1")

        metrics = db.get_metrics()

        return {
            "status": "healthy",
            "database": "connected",
            "workers": metrics["worker_count"],
            "pending_jobs": metrics["pending_jobs"],
            "running_jobs": metrics["running_jobs"]
        }

    except Exception as e:

        logger.error(f"Health check failed: {e}")

        raise HTTPException(
            status_code=500,
            detail="System unhealthy"
        )