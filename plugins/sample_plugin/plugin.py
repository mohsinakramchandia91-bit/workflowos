class SamplePlugin:
    name = "Sample Plugin"

    def execute(self, job):
        # Example logic
        print(f"Executing job {job['id']} for tenant {job['tenant_id']}")

        # Simulate business logic
        return {
            "status": "success",
            "processed_job_id": job["id"]
        }