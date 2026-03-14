import os


class Settings:
    """
    Central configuration manager for WorkflowOS
    """

    APP_NAME = "WorkflowOS"

    # Environment
    ENV = os.getenv("ENV", "development")

    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/workflows"
    )

    # Workers
    WORKER_CONCURRENCY = int(os.getenv("WORKER_CONCURRENCY", 4))

    # Job configuration
    JOB_TIMEOUT = int(os.getenv("JOB_TIMEOUT", 300))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()