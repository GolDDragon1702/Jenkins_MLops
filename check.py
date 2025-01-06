import sys
from fastapi.testclient import TestClient
from api import app

test_cases = [
    (1, {"is_prime": False}),
    (2, {"is_prime": True}),
    (4, {"is_prime": False}),
    (7, {"is_prime": True}),
    (24, {"is_prime": False}),
    (37, {"is_prime": True}),
    (49, {"is_prime": False}),
    (53, {"is_prime": True}),
    (100, {"is_prime": False}),
    (997, {"is_prime": True}),
]

client = TestClient(app)

def run_tests():
    for number, expected in test_cases:
        response = client.get(f"/check_prime/{number}")
        
        # Handle error response for non-integer inputs
        if isinstance(number, float):
            if response.status_code == 400:  # Expected failure
                print(f"Test passed for input {number}")
                continue
            else:
                print(f"Test failed for input {number}: {response.json()} != {expected}")
                sys.exit(1)  # Failure

        # Check if the response is correct for valid integer inputs
        if response.status_code != 200 or response.json() != expected:
            print(f"Test failed for input {number}: {response.json()} != {expected}")
            sys.exit(1)  # Failure
        print(f"Test passed for input {number}")
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
