import logging
import json
import sys
from datetime import datetime


class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": record.name,
            "message": record.getMessage(),
        }

        # include extra fields if present
        if hasattr(record, "job_id"):
            log_record["job_id"] = record.job_id

        if hasattr(record, "worker_id"):
            log_record["worker_id"] = record.worker_id

        return json.dumps(log_record)


def get_logger(name: str):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.propagate = False

    return logger