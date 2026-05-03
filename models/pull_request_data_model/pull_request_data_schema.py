create_pr_schema = {
    "type": "object",
    "properties": {
        "url": {"type": "string"},
        "id": {"type": "integer"},
        "number": {"type": "integer"},
        "state": {"type": "string"},
        "locked": {"type": "boolean"},
        "title": {"type": "string"},
        "user": {"type": "object"},
        "repo": {"type": "object"},
        "head": {"type": "object"},
        "base": {"type": "object"}
    },
    "required": [ "id", "number", "state", "title", "head", "base" ]
}


