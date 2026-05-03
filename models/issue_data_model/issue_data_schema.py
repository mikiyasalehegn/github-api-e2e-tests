create_issue_response_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "state": {"type": "string"},
        "body": {"type": "string"},
        "title": {"type": "string"},
        "locked": {"type": "boolean"},
        "user": {"type": "object"},
        "assignee": {"type": "object"},
    },
    "required": ["id", "state", "body", "title", "locked", "user", "assignee"],
}

