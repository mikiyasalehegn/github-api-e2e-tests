create_repo_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "full_name": {"type": "string"},
        "owner": {"type": "object"},
        "description": {"type": "string"},
        "private": {"type": "boolean"},
    },
    "required": [ "id", "name", "full_name", "owner", "description", "private" ],
}


