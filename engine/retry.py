import time
import logging

logger = logging.getLogger(__name__)


def retry(func, retries=3, delay=2):
    """
    Retry wrapper for jobs and tasks
    """

    for attempt in range(retries):
        try:
            return func()

        except Exception as e:

            logger.warning(
                f"Retry attempt {attempt + 1} failed: {str(e)}"
            )

            if attempt == retries - 1:
                raise

            time.sleep(delay)