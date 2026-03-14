from fastapi import APIRouter

router = APIRouter()


@router.get("/metrics")
def metrics():
    """
    Basic monitoring metrics endpoint
    """

    return {
        "status": "ok",
        "workers": 1,
        "queue_size": 0
    }