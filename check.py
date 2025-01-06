import sys
from fastapi.testclient import TestClient
from Api import app

test_cases = [
    (1, {"is_prime": False}),
    (2, {"is_prime": True}),
    (3, {"is_prime": True}),
    (49, {"is_prime": False}),
    (53, {"is_prime": True}),
    (100, {"is_prime": False}),
    (0.1, {"is_prime": False}),
    (1.5, {"is_prime": False}),
    (-0.5, {"detail": [{"type": "type_error", "loc": ["path", "number"], "msg": "value is not a valid integer", "input": "string_input"}]}),
    (-5, {"detail": [{"type": "type_error", "loc": ["path", "number"], "msg": "value is not a valid integer", "input": "string_input"}]}),
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
