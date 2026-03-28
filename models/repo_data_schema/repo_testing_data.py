class GetRepoResponse:
    def __init__(self, response_json):
        self.owner = response_json["owner"]["login"]
        self.full_name = response_json.get("full_name")


class CreateRepoData:
    def __init__(self, repo_name, description, path, private=False, is_template=True):
        self.repo_name = repo_name
        self.description = description
        self.path = path
        self.private = private
        self.is_template = is_template

    def to_dict(self):
        return {
            "name": self.repo_name,
            "description": self.description,
            "homepage": self.path,
            "private": self.private,
            "is_template": self.is_template,
        }

class UpdateRepoData:
    def __init__(self, new_repo_name, new_description):
        self.new_repo_name = new_repo_name
        self.new_description = new_description

    def to_dict(self):
        return {
            "name": self.new_repo_name,
            "description": self.new_description,
        }

class CreateRepoResponse:
    def __init__(self, response_json):
        self.name = response_json.get("name")
        self.description = response_json.get("description")
        self.path = response_json.get("homepage")
        self.private = response_json.get("private")