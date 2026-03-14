from pydantic import BaseModel


class JobCreateRequest(BaseModel):
    plugin_name: str


class JobResponse(BaseModel):
    id: int
    plugin: str
    status: str
    progress: int
    message: str | None = None
    result: str | None = None
    error: str | None = None
    created: float
    finished: float | None = None