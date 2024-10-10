import time
import sys
import tracemalloc
import matplotlib.pyplot as plt


# Unoptimized recursive Fibonacci function
def fib_recursive(n):
    if n <= 1:
        return n
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)


# Memoized Fibonacci function
def fib_memoization(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    else:
        memo[n] = fib_memoization(n - 1, memo) + fib_memoization(n - 2, memo)
        return memo[n]

# Optimized caching Fibonacci function
def fib_speed_calculation(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# Function to measure time and memory usage using trace malloc
def measure_performance(func, n, label):
    # Start tracking memory allocations
    tracemalloc.start()

    # Measure time
    start_time = time.time()

    result = func(n)

    end_time = time.time()

    # Stop tracing memory allocations
    current, peak = tracemalloc.get_traced_memory()

    # Convert memory from bytes to MB
    current_memory_mb = current / 10 ** 6
    peak_memory_mb = peak / 10 ** 6

    time_taken = end_time - start_time

    # Stop tracing memory allocations
    tracemalloc.stop()

    # Output performance data
    print(f"\n{label}:")
    print(f"Result: {result}")
    print(f"Time taken: {(time_taken):.8f} seconds")
    # Print memoization cache size only for the memoized version
    if label == "Memoized Fibonacci":
        memory_of_memo_dict = sys.getsizeof(func.__defaults__[0])
        print(f"Memory used by memoization cache: {memory_of_memo_dict} bytes")
    print(f"Current memory usage: {current_memory_mb:.6f} MB")
    print(f"Peak memory usage: {peak_memory_mb:.6f} MB\n")


    return round(time_taken, 6)


# Stress testing both functions
def stress_test(n, unoptimized_times, memoized_times):
    print(f"Testing Fibonacci for n = {n}")

    # Test unoptimized recursive version
    try:
        unoptimized_times.append(measure_performance(fib_recursive, n, "Unoptimized Recursive Fibonacci"))
    except RecursionError:
        print("Unoptimized Recursive Fibonacci exceeded recursion limit.")

    # Test memoized version
    memoized_times.append(measure_performance(fib_memoization, n, "Memoized Fibonacci"))

    # Test Speed version
    measure_performance(fib_speed_calculation, n, "Speed Fibonacci")

def plot_result(n_values, unoptimized_times, memoized_times):
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, unoptimized_times, label="Unoptimized Recursive Fibonacci", marker='o')
    plt.plot(n_values, memoized_times, label="Memoized Fibonacci", marker='o')

    # Adding labels and title
    plt.title('Time Comparison: Unoptimized Recursive vs Memoized Fibonacci')
    plt.xlabel('n (Input Size)')
    plt.ylabel('Time (seconds)')
    plt.yscale('log')  # Log scale for better comparison since memoized times are much smaller
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.show()


# Run stress test for a large value of n
if __name__ == "__main__":
    n_values = [10, 20, 30, 35, 40, 45] # Add or delete the n number of fib
    unoptimized_times = []
    memoized_times = []

    for n in n_values:
        stress_test(n, unoptimized_times, memoized_times)  # You can adjust n to stress test further

    plot_result(n_values, unoptimized_times, memoized_times)
