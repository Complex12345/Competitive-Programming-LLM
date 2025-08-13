from kaggle.api.kaggle_api_extended import KaggleApi
import time
import sys
import json
import tracemalloc

if len(sys.argv) < 2:
    print("Usage: python kaggle_poll.py <TEST_CASE>")
    sys.exit(1)

TEST_CASE = sys.argv[1]
KERNEL_REF = "nlmbu5/my-notebook"  # change if your kernel path is different

api = KaggleApi()
api.authenticate()

# Poll until the kernel finishes
status = api.kernels_status(KERNEL_REF)
while status['status'] in ('running', 'pending'):
    print(f"Current status: {status['status']}")
    time.sleep(5)
    status = api.kernels_status(KERNEL_REF)

print(f"Kernel finished with status: {status['status']}")

# Download output notebook
api.kernels_output(KERNEL_REF, path='output_notebook.ipynb', force=True)

# Analyze notebook memory and time
tracemalloc.start()
start_time = time.time()

with open('output_notebook.ipynb', 'r', encoding='utf-8') as f:
    notebook_data = json.load(f)

cell_count = len(notebook_data.get('cells', []))
print(f"Notebook has {cell_count} cells.")

current, peak = tracemalloc.get_traced_memory()
end_time = time.time()
tracemalloc.stop()

print(f"Execution time: {end_time - start_time:.4f} seconds")
print(f"Peak memory usage: {peak / 1024:.2f} KB")
