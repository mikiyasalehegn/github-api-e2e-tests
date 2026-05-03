from jsonschema import validate


def assert_data_schema(response, schema):
    validate(instance=response.json(), schema=schema)

def assert_key(response, key_to_validate, expected_value, is_nested = False, index = None):
    response = response.json() if is_nested and index else response.json()[index]
    assert response.get(key_to_validate, f"{key_to_validate} doesn't exist") == expected_value, \
        f" Expected {expected_value}, got {response.json().get(key_to_validate)}"

def assert_error_messages(response, expected_messages):
    assert response.json().get("message") == expected_messages, \
        f"Expected {expected_messages}, got {response.json().get('message')}"
