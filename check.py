import sys
from fastapi.testclient import TestClient
from Api import app

# Danh sách test cases
test_cases = [
    (1, {"is_prime": False}),
    (2, {"is_prime": True}),
    (3, {"is_prime": True}),
    (4, {"is_prime": False}),
    (5, {"is_prime": True}),
    (100, {"is_prime": False}),
    (101, {"is_prime": True}),
    (997, {"is_prime": True}),
    (0.1, {"is_prime": False}),
    (1.5, {"is_prime": False})
]

client = TestClient(app)

def run_tests():
    for number, expected in test_cases:
        response = client.get(f"/check_prime/{number}")
        if response.status_code != 200 or response.json() != expected:
            print(f"Test failed for input {number}: {response.json()} != {expected}")
            sys.exit(1)  # Thất bại
        print(f"Test passed for input {number}")
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
