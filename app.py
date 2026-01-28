from flask import Flask, request, jsonify
import time
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

# Import your algorithm functions
from factorial import linear_search, bubble_sort, binary_search, nested_loops

app = Flask(__name__)

# Mapping from query string → actual function
ALGORITHMS = {
    "linear":       linear_search,
    "linearsearch": linear_search,
    "bubble":       bubble_sort,
    "bubblesort":   bubble_sort,
    "bubble_sort":  bubble_sort,
    "binary":       binary_search,
    "binarysearch": binary_search,
    "nested":       nested_loops,
    "nestedloops":  nested_loops,
    "exponential":  nested_loops,   # treat as O(n²) for now
}


def measure_times(algorithm_func, max_n, num_steps):
    """
    Measures real running time for different input sizes
    Returns: input_sizes (list), times (list)
    """
    # Create roughly evenly spaced sizes
    input_sizes = np.linspace(10, max_n, num_steps, dtype=int).tolist()
    
    times = []
    
    for n in input_sizes:
        # Prepare data outside timing 
        if algorithm_func == binary_search:
            arr = sorted(np.random.randint(0, 100000, n))  # large range to avoid duplicates
            target = arr[-1]
            def timed_func():
                binary_search_work(arr, target)  # avoid recreating array
        elif algorithm_func == bubble_sort:
            def timed_func():
                bubble_sort(n)
        elif algorithm_func == linear_search:
            def timed_func():
                linear_search(n)
        elif algorithm_func == nested_loops:
            def timed_func():
                nested_loops(n)
        else:
            def timed_func():
                algorithm_func(n)

        # Measure
        start = time.perf_counter()
        timed_func()
        end = time.perf_counter()
        
        times.append(end - start)

    return input_sizes, times

def binary_search_work(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


@app.route('/analyze', methods=['GET'])
def analyze():
    start_total = time.perf_counter()

    # Get parameters
    algo   = request.args.get('algo',   default='linear',   type=str).lower().strip()
    n      = request.args.get('n',      default=1000,       type=int)
    steps  = request.args.get('steps',  default=10,         type=int)

    # Basic safety limits
    n      = max(100, min(n, 20000))       # prevent killing the server
    steps  = max(4,  min(steps, 30))

    if algo not in ALGORITHMS:
        return jsonify({
            "status": "error",
            "message": f"Unknown algorithm. Supported: {', '.join(ALGORITHMS.keys())}"
        }), 400

    func = ALGORITHMS[algo]

    # Measure real times
    input_sizes, run_times = measure_times(func, n, steps)

    # Create plot
    plt.figure(figsize=(8, 5))
    plt.plot(input_sizes, run_times, 'o-', color='teal', linewidth=2, markersize=6)
    plt.title(f"Measured Time Complexity – {algo.capitalize()}", fontsize=14)
    plt.xlabel("Input size (n)", fontsize=12)
    plt.ylabel("Running time (seconds)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Convert to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=110, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    total_time = time.perf_counter() - start_total

    return jsonify({
        "status": "success",
        "context": {
            "algorithm": algo,
            "max_n": n,
            "steps": steps,
            "execution_time_seconds": round(total_time, 5)
        },
        "data": {
            "input_sizes": input_sizes,
            "times_seconds": [round(t, 6) for t in run_times]
        },
        "graph_base64": img_base64
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)