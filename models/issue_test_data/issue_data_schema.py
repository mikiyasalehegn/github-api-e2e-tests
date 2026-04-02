create_issue_response_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "state": {"type": "string"},
        "body": {"type": "string"},
        "title": {"type": "string"},
        "locked": {"type": "string"},
        "user": {"type": "string"},
        "creator": {"type": "boolean"},
        "assignee": {"type": "string"}
    },
    "required": ["id", "state", "body", "title", "locked", "creator", "assignee"],
}

