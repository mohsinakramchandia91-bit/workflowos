import time


class SamplePlugin:
    name = "Sample Plugin"
    version = "1.0"
    description = "Demo plugin for WorkflowOS"

    def execute(self, payload, progress_callback):
        """
        Required signature:
        execute(payload: dict, progress_callback: callable)
        """

        progress_callback(0, "Started")

        for i in range(5):
            time.sleep(1)
            progress_callback((i + 1) * 20, f"Step {i+1}/5")

        return {"status": "success"}