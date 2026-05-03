create_webhook_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
    },
    "required": ["name", "id", "type"],
}

update_webhook_data = {
            "add_events": [
                "pull_request",
                "push",
                "issues",
                "star"
            ]
        }