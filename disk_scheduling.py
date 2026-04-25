"""
Lab Assignment-4: Implementation and Analysis of Disk Scheduling Algorithms
Course: Fundamentals of Operating System Lab (ENCA252)
Program: BCA (AI & DS) (Research)

Algorithms implemented:
  1. FCFS   - First Come First Serve
  2. SSTF   - Shortest Seek Time First
  3. SCAN   - Elevator Algorithm
  4. C-SCAN - Circular SCAN
"""


# ─────────────────────────────────────────────────────────────
# Task 1: Input and Disk Request Representation
# ─────────────────────────────────────────────────────────────
def get_input():
    """Get disk request queue, initial head position, and disk size."""
    print("=" * 55)
    print("      DISK SCHEDULING ALGORITHM SIMULATOR")
    print("=" * 55)

    # Input: disk request queue
    while True:
        try:
            raw = input("\nEnter disk request queue (space-separated): ")
            requests = list(map(int, raw.split()))
            if not requests:
                print("  Request queue cannot be empty.")
                continue
            if any(r < 0 for r in requests):
                print("  All requests must be non-negative.")
                continue
            break
        except ValueError:
            print("  Invalid input. Enter integers separated by spaces.")

    # Input: initial head position
    while True:
        try:
            head = int(input("Enter initial head position: "))
            if head < 0:
                print("  Head position must be non-negative.")
                continue
            break
        except ValueError:
            print("  Invalid input. Please enter an integer.")

    # Input: disk size
    while True:
        try:
            disk_size = int(input("Enter disk size (total cylinders, e.g. 200): "))
            if disk_size <= 0:
                print("  Disk size must be a positive integer.")
                continue
            break
        except ValueError:
            print("  Invalid input. Please enter an integer.")

    print(f"\nRequest Queue    : {requests}")
    print(f"Initial Head     : {head}")
    print(f"Disk Size        : {disk_size} cylinders")
    print("-" * 55)

    return requests, head, disk_size


# ─────────────────────────────────────────────────────────────
# Helper: print movement sequence and seek time
# ─────────────────────────────────────────────────────────────
def print_result(algo_name, sequence, seek_time):
    print(f"\n{'─'*55}")
    print(f"  {algo_name}")
    print(f"{'─'*55}")
    print(f"  Movement Sequence : {' → '.join(map(str, sequence))}")
    print(f"  Total Seek Time   : {seek_time} cylinders")


# ─────────────────────────────────────────────────────────────
# Task 2: FCFS - First Come First Serve
# ─────────────────────────────────────────────────────────────
def fcfs(requests, head):
    """
    Service requests in the exact order they arrive.
    Simple but can result in large head movements.
    """
    seek_time = 0
    current = head
    sequence = [head]

    for req in requests:
        seek_time += abs(current - req)
        current = req
        sequence.append(req)

    print_result("FCFS (First Come First Serve)", sequence, seek_time)
    return seek_time


# ─────────────────────────────────────────────────────────────
# Task 3: SSTF - Shortest Seek Time First
# ─────────────────────────────────────────────────────────────
def sstf(requests, head):
    """
    Always service the request closest to the current head position.
    Reduces seek time but may cause starvation of far requests.
    """
    seek_time = 0
    current = head
    remaining = requests.copy()
    sequence = [head]

    while remaining:
        # Find the nearest request to current head
        nearest = min(remaining, key=lambda x: abs(x - current))
        seek_time += abs(current - nearest)
        current = nearest
        sequence.append(nearest)
        remaining.remove(nearest)

    print_result("SSTF (Shortest Seek Time First)", sequence, seek_time)
    return seek_time


# ─────────────────────────────────────────────────────────────
# Task 4: SCAN - Elevator Algorithm
# ─────────────────────────────────────────────────────────────
def scan(requests, head, disk_size):
    """
    Head moves in one direction servicing all requests,
    reaches the end of disk, then reverses direction.
    Like an elevator going up then coming back down.
    """
    seek_time = 0
    current = head
    sequence = [head]

    # Split requests into left and right of head
    left  = sorted([r for r in requests if r < head], reverse=True)
    right = sorted([r for r in requests if r >= head])

    # First go RIGHT (increasing direction)
    for r in right:
        seek_time += abs(current - r)
        current = r
        sequence.append(r)

    # Go to the rightmost end of disk
    seek_time += abs(current - (disk_size - 1))
    current = disk_size - 1
    sequence.append(disk_size - 1)

    # Then go LEFT (decreasing direction)
    for r in left:
        seek_time += abs(current - r)
        current = r
        sequence.append(r)

    print_result("SCAN (Elevator Algorithm)", sequence, seek_time)
    return seek_time


# ─────────────────────────────────────────────────────────────
# Task 5: C-SCAN - Circular SCAN
# ─────────────────────────────────────────────────────────────
def cscan(requests, head, disk_size):
    """
    Head moves in one direction only (right).
    When it reaches the end, it jumps back to cylinder 0
    and continues in the same direction.
    Provides more uniform wait time than SCAN.
    """
    seek_time = 0
    current = head
    sequence = [head]

    # Split requests into left and right of head
    left  = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    # First go RIGHT servicing all requests on right side
    for r in right:
        seek_time += abs(current - r)
        current = r
        sequence.append(r)

    # Go to the rightmost end of disk
    seek_time += abs(current - (disk_size - 1))
    current = disk_size - 1
    sequence.append(disk_size - 1)

    # Jump back to cylinder 0 (the circular jump)
    seek_time += disk_size - 1
    current = 0
    sequence.append(0)

    # Now service the left requests (which are now on the right of 0)
    for r in left:
        seek_time += abs(current - r)
        current = r
        sequence.append(r)

    print_result("C-SCAN (Circular SCAN)", sequence, seek_time)
    return seek_time


# ─────────────────────────────────────────────────────────────
# Task 6 & 7: Performance Comparison and Result Analysis
# ─────────────────────────────────────────────────────────────
def compare_algorithms(requests, head, disk_size):
    """Run all algorithms and display comparison with analysis."""
    print("\n" + "=" * 55)
    print("   RUNNING ALL ALGORITHMS")
    print("=" * 55)

    results = {
        "FCFS"   : fcfs(requests, head),
        "SSTF"   : sstf(requests, head),
        "SCAN"   : scan(requests, head, disk_size),
        "C-SCAN" : cscan(requests, head, disk_size),
    }

    # ── Comparison Table ──────────────────────────────────────
    print("\n" + "=" * 55)
    print("   PERFORMANCE COMPARISON SUMMARY")
    print("=" * 55)
    print(f"{'Algorithm':<12} {'Total Seek Time':>16} {'Performance':>14}")
    print("-" * 44)

    min_seek = min(results.values())
    for algo, seek in results.items():
        bar = "█" * (seek // 10)
        tag = " ← BEST" if seek == min_seek else ""
        print(f"{algo:<12} {seek:>16} cylinders{tag}")

    # ── Result Analysis ───────────────────────────────────────
    best_algo  = min(results, key=results.get)
    worst_algo = max(results, key=results.get)

    print("\n" + "=" * 55)
    print("   RESULT ANALYSIS")
    print("=" * 55)
    print(f"  Best  Algorithm : {best_algo}  ({results[best_algo]} cylinders)")
    print(f"  Worst Algorithm : {worst_algo} ({results[worst_algo]} cylinders)")

    print("""
  Conclusions
  ───────────
  • FCFS    → Simplest algorithm. Services requests in arrival
              order. Easy to implement but causes high seek time
              due to random head movement (no optimization).

  • SSTF    → Always picks the closest request. Gives the lowest
              or near-lowest seek time but can starve far requests
              (they keep getting skipped). Not fair.

  • SCAN    → Head sweeps back and forth like an elevator. Good
              balance of performance and fairness. No starvation.
              Used widely in real operating systems.

  • C-SCAN  → Only moves in one direction, then jumps to start.
              More uniform wait time than SCAN. Fair to all
              requests. Slightly higher seek time due to the jump.
    """)


# ─────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    requests, head, disk_size = get_input()
    compare_algorithms(requests, head, disk_size)
