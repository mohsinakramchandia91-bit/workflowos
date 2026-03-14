from fastapi import FastAPI
from api.routes import router
from core.database import DatabaseManager
from core.logger import get_logger

logger = get_logger("api")
db = DatabaseManager(logger)

app = FastAPI(
    title="WorkflowOS",
    version="1.0.0",
    description="Distributed Job Processing Engine"
)

app.include_router(router)

# ---------------------------
# HEALTH CHECK
# ---------------------------

@app.get("/health")
def health():
    try:
        with db._connect() as conn:
            return {"status": "healthy"}
    except Exception:
        return {"status": "database_error"}


# ---------------------------
# METRICS
# ---------------------------

@app.get("/metrics")
def metrics():
    return db.get_metrics()