import time
import signal
import sys


class WorkerEngine:
    def __init__(self, db, plugin_manager, logger):
        self.db = db
        self.plugin_manager = plugin_manager
        self.logger = logger
        self.worker_id = None
        self.shutdown_requested = False

    # ================= SIGNAL HANDLING =================

    def _handle_shutdown(self, signum, frame):
        self.logger.info("Shutdown signal received. Worker will stop after current job.")
        self.shutdown_requested = True

    # ================= DAEMON =================

    def start_daemon(self):

        # Register signals
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

        # Register worker
        self.worker_id = self.db.register_worker()

        self.logger.info(f"Worker {self.worker_id} started daemon mode.")

        while not self.shutdown_requested:

            try:

                # Heartbeat + cleanup
                self.db.cleanup_dead_workers()
                self.db.update_heartbeat(self.worker_id)

                # Timeout enforcement
                self.db.check_timeouts()

                job_id = self.db.claim_job(self.worker_id)

                if job_id:
                    self.execute_job(job_id)

                time.sleep(2)

            except Exception as e:
                self.logger.error(f"Worker loop error: {e}")
                time.sleep(2)

        self.logger.info("Worker shutdown completed.")
        sys.exit(0)

    # ================= EXECUTE JOB =================

    def execute_job(self, job_id):

        try:

            job = self.db.get_job(job_id)

            if not job:
                return

            plugin_name = job["plugin"]

            plugin = self.plugin_manager.get_plugin(plugin_name)

            if not plugin:
                raise Exception(f"Plugin not found: {plugin_name}")

            self.logger.info(
                f"Worker {self.worker_id} executing job {job_id}"
            )

            result = plugin.execute(job)

            self.db.complete_job(job_id, result)

            self.logger.info(
                f"Worker {self.worker_id} finished job {job_id}"
            )

        except Exception as e:

            self.db.fail_job(job_id, str(e))

            self.logger.error(
                f"Job {job_id} failed: {e}"
            )