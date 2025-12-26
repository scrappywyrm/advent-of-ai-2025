
import random
import time

def simulate_request():
    """Simulates a request to the ticket system."""
    # Simulate network timeout (15% chance)
    if random.random() < 0.15:
        print("[ERROR] NetworkTimeout")
        return "NetworkTimeout"

    # Simulate database error (5% chance)
    if random.random() < 0.05:
        print("[ERROR] DatabaseError")
        return "DatabaseError"

    # Simulate success
    print("[200 OK]")
    return "Success"

def main():
    """Runs the load test simulation."""
    total_requests = 100
    success_count = 0
    failure_types = {}

    for _ in range(total_requests):
        result = simulate_request()
        if result == "Success":
            success_count += 1
        else:
            failure_types[result] = failure_types.get(result, 0) + 1
        time.sleep(0.01)  # Simulate some processing time

    # Generate summary report
    success_rate = (success_count / total_requests) * 100
    print("\n--- Summary Report ---")
    print(f"Total Requests: {total_requests}")
    print(f"Success Rate: {success_rate:.2f}%")
    print("Failure Types:")
    for error_type, count in failure_types.items():
        print(f"  - {error_type}: {count}")

if __name__ == "__main__":
    main()
