import pytest
from api import WebhookApi
from base import BaseTest
from models import CreateWebhookData, CreateWebhookResponse, create_webhook_schema, update_webhook_data, UpdateWebhookResponse
from utils.config import USERNAME
from utils import assert_data_schema
import logging


logger = logging.getLogger(__name__)




@pytest.mark.usefixtures("create_temporary_repo")
class TestWebhookFlow(BaseTest):
    webhook_id = None

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.webhook_api = WebhookApi(self.client)

    def test_github_webhook_flow(self, create_temporary_repo):
        # get uuid
        uuid = CreateWebhookData.create_uuid()

         # -------------------- Test create webhook --------------------
        repository_name = create_temporary_repo
        payload = CreateWebhookData(name="web", uuid=uuid)
        response = self.webhook_api.create_github_webhook(owner=USERNAME, repo=repository_name, data=payload.to_dict())
        webhook_resp = CreateWebhookResponse(response.json())
        logger.info(f"create webhook response: {response.text}")
        assert response.status_code == 201
        assert_data_schema(response, create_webhook_schema)
        assert webhook_resp.type == "Repository"
        assert webhook_resp.name == "web"
        self.webhook_id = webhook_resp.id

        # -------------------- Test if the repo exists --------------------
        response = self.webhook_api.get_github_webhook(owner=USERNAME, repo=repository_name, hook_id=self.webhook_id)
        assert response.status_code == 200
        assert_data_schema(response, create_webhook_schema)


        # -------------------- Test update webhook --------------------
        update_resp = self.webhook_api.update_github_webhook(owner=USERNAME, repo=repository_name,
                                                             hook_id=webhook_resp.id, data=update_webhook_data)
        update_webhook_resp = UpdateWebhookResponse(update_resp.json())

        update_resp.status_code = 200
        logger.info(f"update webhook response: {update_resp.text}")
        assert update_resp.json().get("type") == "Repository"
        assert update_resp.json().get("name") == "web"
        assert update_webhook_resp.events == update_webhook_data["add_events"]


        # -------------------- Test ping webhook --------------------
        ping_resp = self.webhook_api.ping_webhook(owner=USERNAME, repo=repository_name, hook_id=self.webhook_id)
        print(f"Ping[{self.webhook_id}] response: {ping_resp}")
        assert ping_resp.status_code == 204

        # -------------------- Test delete webhook --------------------
        delete_webhook_resp = self.webhook_api.delete_github_webhook(owner=USERNAME, repo=repository_name,
                                                                     hook_id=self.webhook_id)
        delete_webhook_resp.status_code = 204


        # --------------------Verify the webhook is deleted --------------------Verify
        get_webhook_resp = self.webhook_api.get_github_webhook(owner=USERNAME, repo=repository_name,
                                                               hook_id=self.webhook_id)
        get_webhook_resp.status_code = 404

