class CreateIssuePayload:

    def __init__(self, title, body, assignees, labels):
        self.title = title
        self.body = body
        self.assignees = assignees
        self.labels = labels

    def to_dict(self):
        return {
        "title": self.title,
        "body": self.body,
        "assignees": [f"{self.assignees}"],
        "labels": self.labels
    }


class IssueResponseData:
    def __init__(self, response_json):
        self.state = response_json.get("state")
        self.body = response_json.get("body")
        self.title = response_json.get("title")
        self.user = response_json.get("user")
        self.labels = response_json.get("labels")
        self.locked = response_json.get("locked")
        self.creator = response_json.get("creator")
        self.assignee = response_json.get("assignee")


class IssueTestData:
    body = "Github API Automation Test Run!"
    title = "Test Github Issue"
    labels = ["automated-test", "QA-internal"]
    new_label = ["bug"]
    new_body = "Updated description"
    new_title = "Updated issue title",
    lock_reason= {
        "lock_reason": "resolved"
    }


class UpdateIssuePayload:
    def __init__(self,body, labels: list[str]):
        # self.title = title   # Updating title has a bug
        self.body = body
        self.labels = labels

    def to_dict(self):
        return {
            # "title": self.title,   # Updating title has a bug
            "body": self.body,
            "labels": self.labels
        }
