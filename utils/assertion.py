from jsonschema import validate


def assert_status_code(response, expected_code):
    assert response.status_code == expected_code, f" Expected {expected_code}, got {response.status_code}"

def assert_data_schema(response, schema):
    validate(instance=response.json(), schema=schema)

def assert_key(response, key_to_validate, expected_value, is_nested = False, index = None):
    response = response.json() if is_nested and index else response.json()[index]
    assert response.get(key_to_validate, f"{key_to_validate} doesn't exist") == expected_value, \
        f" Expected {expected_value}, got {response.json().get(key_to_validate)}"

def assert_pet_statuses(response, expected_statuses):
    statuses = [pet.get("status") for pet in response.json()]
    assert all(stat == expected_statuses for stat in statuses), f"Expected {expected_statuses}, got {statuses}"

def assert_error_messages(response, expected_messages):
    assert response.json().get("message") == expected_messages, \
        f"Expected {expected_messages}, got {response.json().get('message')}"