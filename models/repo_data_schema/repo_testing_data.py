class GetRepoResponse:
    def __init__(self, response_json):
        self.owner = response_json["owner"]["login"]
        self.full_name = response_json.get("full_name")