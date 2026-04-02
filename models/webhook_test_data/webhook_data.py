import requests


class CreateWebhookData:
    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid

    def to_dict(self):
        return {
                "name": self.name,
                "active": True,
                "events": [
                    "push",
                    "pull_request"
                    ],
                "config": {
                    "content_type": "json",
                    "url": f"https://webhook.site/{self.uuid}",
                    "insecure_ssl": "0"
                }
            }

    @staticmethod
    def create_uuid():
        resp = requests.post("https://webhook.site/token", data='')

        if resp.status_code in [201, 200]:
            return resp.json()["uuid"]
        else:
            raise Exception(f"Failed to create UUID: {resp.status_code}")


class CreateWebhookResponse:

    def __init__(self, response_json):
        self.type = response_json.get("type")
        self.name = response_json.get("name")
        self.id = response_json.get("id")


class UpdateWebhookResponse:
    def __init__(self, response_json):
        self.type = response_json.get("type")
        self.name = response_json.get("name")
        self.events = response_json.get("events")
