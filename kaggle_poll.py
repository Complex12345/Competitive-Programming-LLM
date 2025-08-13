import time
import json
import subprocess
from kaggle.api.kaggle_api_extended import KaggleApi
import sys

NOTEBOOK_PATH = "notebook.ipynb"  # replace with your notebook filename
OUTPUT_PATH = "output_notebook.ipynb"
KERNEL_REF = "nlmbu5/my-notebook"
TEST_CASE = sys.argv[1] if len(sys.argv) > 1 else "default"

# Authenticate Kaggle
api = KaggleApi()
api.authenticate()

# Poll until kernel finishes
status = api.kernel_status(KERNEL_REF)
while status['status'] in ('running', 'pending'):
    print(f"Current status: {status['status']}")
    time.sleep(5)
    status = api.kernel_status(KERNEL_REF)

print(f"Kernel finished with status: {status['status']}")

# Download notebook output
api.kernels_output(kernel=KERNEL_REF, path=".", force=True)
print(f"Downloaded output to {OUTPUT_PATH}")

# Run analysis
subprocess.run(["python", "analyze_solution.py", TEST_CASE], check=True)
