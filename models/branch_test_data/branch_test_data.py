from importlib.util import source_hash


class BranchProtectionTestData:

    def __init__(self, enforce_admins=True, allow_force_pushes=True,
                 allow_deletions=True, required_status_checks=None, review_count=1):

        self.enforce_admins = enforce_admins
        self.allow_force_pushes = allow_force_pushes
        self.allow_deletions = allow_deletions
        self.required_status_checks = required_status_checks
        self.review_count = review_count

    def to_dict(self):
       return {
            "enforce_admins": self.enforce_admins,
            "required_pull_request_reviews": {"required_approving_review_count": self.review_count},
            "required_status_checks": self.required_status_checks,
            "allow_force_pushes": self.allow_force_pushes,
            "allow_deletions": self.allow_deletions,
            "restrictions": None
        }


class BranchTestResponse:
    def __init__(self, response_json):
        self.enforce_admins = response_json.get("enforce_admins")
        self.required_pull_request_reviews = response_json.get("required_pull_request_reviews")
        self.status_checks = response_json.get("status_checks")
        self.allow_force_pushes = response_json.get("allow_force_pushes")
        self.allow_deletions = response_json.get("allow_deletions")


class BranchTestData:
    branch_name = "Feature-branch"
    new_branch_name = "New-branch"


class CreateBranchTestData:
    def __init__(self, name, source_sha):
        self.name = name
        self.source_sha = source_sha

    def to_dict(self):
       return {
            "ref": f"refs/heads/{self.name}", # Required format
            "sha": self.source_sha
        }








