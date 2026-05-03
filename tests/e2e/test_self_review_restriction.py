import time
import pytest
from api import ContentApi, BranchApi, PullRequestApi
from base import BaseTest
from models.pullrequest_model.pr_payload_model import CreatePrPayload
from test_data import PullRequestDataTest
from utils import USERNAME
import logging


logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("feature_branch_ready_for_pr")
@pytest.mark.repo_config(with_readme=True)
class TestSelfReviewRestriction(BaseTest):
    def setup_method(self):
        super().setup_method()

        client = self.get_client()
        self.content_api = ContentApi(client)
        self.branch_api = BranchApi(client)
        self.pr_api = PullRequestApi(client)

    def test_self_review_restriction(self, feature_branch_ready_for_pr):
        repo_name, branch_name = feature_branch_ready_for_pr
        file_resp = self.content_api.create_file(owner=USERNAME, repo=repo_name, path=PullRequestDataTest.file_name,
                                     message=PullRequestDataTest.default_message,
                                     content=PullRequestDataTest.default_content, branch=branch_name)

        file_resp.status_code = 201
        time.sleep(1)

        # ---------------------- Create pr ----------------------
        payload = CreatePrPayload(title=PullRequestDataTest.default_title, head=branch_name, base="main",
                                  body=PullRequestDataTest.pr_body)
        pr_response = self.pr_api.create_pull_request(owner=USERNAME, repo=repo_name, data=payload.to_dict())
        pr_response.status_code = 201
        pr_response.json()["state"] = "open"
        pr_response.json()["title"] = PullRequestDataTest.default_title
        pr_number = pr_response.json()["number"]
        time.sleep(1)

        # ---------------------- approve the pr using the same token ----------------------
        payload = {
        "body": "Approved via automation",
        "event": "APPROVE"
        }

        pr_approve_resp = self.pr_api.approve_pull_request(owner=USERNAME, repo=repo_name, pr_number= pr_number,
                                                           data=payload)
        logger.info(f"pr_approve_resp data: {pr_approve_resp.text}")
        assert pr_approve_resp.status_code == 422
        assert "Can not approve your own pull request" in pr_approve_resp.json()["errors"][0]
