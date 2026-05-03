class UpdateUserDataModel:

    def __init__(self, twitter_username, bio):
        self.twitter_username = twitter_username
        self.bio = bio

    def to_dict(self):
        return {
            "twitter_username": self.twitter_username,
            "bio": self.bio
        }


class UpdateUserResponse:

    def __init__(self, response_json):
        self.login = response_json.get("login")
        self.twitter_username = response_json.get("twitter_username")
        self.bio = response_json.get("bio")


class GetUserResponse:

    def __init__(self, response_json):
        self.login = response_json.get("login")
        self.type = response_json.get("type")
        self.public_repos = response_json.get("public_repos")
        self.total_private_repos = response_json.get("total_private_repos")

