class CreateIssuePayload:

    def __init__(self, title, body, assignees, milestone):
        self.title = title
        self.body = body
        self.assignees = assignees
        self.milestone = milestone

    def to_dict(self):
        return {
        "title": self.title,
        "body": self.body,
        "assignees": f"{[self.assignees]}",
        "milestone": self.milestone,
        "labels": ["automated-test", "QA-internal"]
    }


class IssueResponseData:
    def __init__(self, state, body, title, user, labels, locked, creator, assignee):
        self.state = state
        self.body = body
        self.title = title
        self.user = user
        self.labels = labels
        self.locked = locked
        self.creator = creator
        self.assignee = assignee


class IssueTestData:
    body = "Github API Automation Test Run!"
    title = "Test Github Issue"

