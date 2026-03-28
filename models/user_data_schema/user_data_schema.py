get_user_data_schema = {
    "type": "object",
    "properties": {
        "login": {"type": "string"},
        "id": {"type": "integer"},
        "type": {"type": "string"},
        "public_repos": {"type": "integer"},
        "total_private_repos": {"type": "integer"},
        "owned_private_repos": {"type": "integer"},
    },
    "required": ["login", "id", "type", "public_repos", "total_private_repos", "owned_private_repos"],
}