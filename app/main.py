import sys
from core.logger import get_logger
from core.database import DatabaseManager
from plugins.plugin_manager import PluginManager
from engine.workers import WorkerEngine
from core.config import PLUGINS_PATH


def run_worker_mode():
    logger = get_logger("worker")
    db = DatabaseManager(logger)
    plugin_manager = PluginManager(PLUGINS_PATH, logger)

    # IMPORTANT: correct argument order
    engine = WorkerEngine(db, plugin_manager, logger)
    engine.start_daemon()


def run_core_mode():
    logger = get_logger("core")
    db = DatabaseManager(logger)
    plugin_manager = PluginManager(PLUGINS_PATH, logger)

    job_id = db.add_job(plugin_name="Sample Plugin")
    logger.info(f"Created job {job_id}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "run-worker":
        run_worker_mode()
    else:
        run_core_mode()


if __name__ == "__main__":
    main()