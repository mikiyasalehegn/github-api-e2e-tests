update_branch_protection_schema = {
    "type": "object",
    "properties": {
        "restrictions": {"type": "object"},
        "required_pull_request_reviews": {"type": "object"},
        "required_status_checks": {"type": "object"},
        "enforce_admins": {"type": "object"},
        "allow_deletions": {"type": "object"},
        "allow_force_pushes": {"type": "object"}
    },
    "required": ["required_pull_request_reviews", "enforce_admins", "allow_deletions", "allow_force_pushes"],
}