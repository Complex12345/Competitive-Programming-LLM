from kaggle.api.kaggle_api_extended import KaggleApi
import time
import subprocess
import sys

OWNER_SLUG = "nlmbu5"
KERNEL_SLUG = "my-notebook"
OUTPUT_PATH = "output_notebook.ipynb"
TEST_CASE = sys.argv[1] if len(sys.argv) > 1 else "default"

api = KaggleApi()
api.authenticate()

# Poll until the kernel finishes
status = api.kernels_status(owner_slug=OWNER_SLUG, kernel_slug=KERNEL_SLUG)
while status['status'] in ('running', 'pending'):
    print(f"Current status: {status['status']}")
    time.sleep(5)
    status = api.kernels_status(owner_slug=OWNER_SLUG, kernel_slug=KERNEL_SLUG)

print(f"Kernel finished with status: {status['status']}")

# Download notebook output
api.kernels_output(owner_slug=OWNER_SLUG, kernel_slug=KERNEL_SLUG, path=".", force=True)
print(f"Downloaded output to {OUTPUT_PATH}")

# Run analysis
subprocess.run(["python", "analyze_solution.py", TEST_CASE], check=True)
