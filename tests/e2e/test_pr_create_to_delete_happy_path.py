import time
import pytest
from api import PullRequestApi, ContentApi, BranchApi
from base import BaseTest
from utils import USERNAME
from test_data import PullRequestDataTest
import logging


logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("feature_branch_ready_for_pr")
@pytest.mark.repo_config(with_readme=True)
class TestPrCreateToDeleteHappyPathTests(BaseTest):

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.content_api = ContentApi(self.client)
        self.pr_api = PullRequestApi(self.client)
        self.branch_api = BranchApi(self.client)

    def test_pr_create_to_delete_happy_path(self, feature_branch_ready_for_pr):
        repo_name, branch_name = feature_branch_ready_for_pr

        # Add a Commit (PRs require a difference between branches)
        file_resp = self.content_api.create_file(owner=USERNAME, repo=repo_name, path=PullRequestDataTest.file_name,
                                     message=PullRequestDataTest.default_message,
                                     content=PullRequestDataTest.default_content, branch=branch_name)

        file_resp.status_code = 201
        time.sleep(1)

        # ---------------------- Create pr ----------------------
        payload = {
                    "title": PullRequestDataTest.default_title,
                    "head": branch_name,
                    "base": "main",
                    "body": PullRequestDataTest.pr_body
                }
        pr_response = self.pr_api.create_pull_request(owner=USERNAME, repo=repo_name, data=payload)
        pr_response.status_code = 201
        pr_response.json()["state"] = "open"
        pr_response.json()["title"] = PullRequestDataTest.default_title
        pr_number = pr_response.json()["number"]

        # ---------------------- List pr files ------------------
        file_resp = self.pr_api.list_pr_files(owner=USERNAME, repo=repo_name, pr_number=pr_number)
        file_resp.status_code = 200
        file_resp.json()[0]["filename"] = PullRequestDataTest.file_name

        # ---------------------- Update pr ------------------
        update_payload = {"title": PullRequestDataTest.updated_pr_title, "body": PullRequestDataTest.updated_pr_body}
        update_pr_resp = self.pr_api.update_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_number,
                                                         data=update_payload)
        logger.info(f"update_pr_resp data: {update_pr_resp.text}")
        update_pr_resp.status_code = 202
        update_pr_resp.json()["title"] = PullRequestDataTest.updated_pr_title
        update_pr_resp.json()["body"] = PullRequestDataTest.updated_pr_body

        # ---------------------- Merge pr ------------------
        merge_pr_resp = self.pr_api.merge_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_number)
        assert merge_pr_resp.status_code == 200

        # ---------------------- Verify the pr is merged ------------------
        get_merged_pr = self.pr_api.get_merged_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_number)
        assert get_merged_pr.status_code == 204


        # ---------------------- Delete the pr branch ------------------
        delete_branch_resp = self.branch_api.delete_branch(owner=USERNAME, repo=repo_name, branch_name=branch_name)
        delete_branch_resp.status_code = 204

        # -------------------- Check a branch is erased --------------------
        get_branch_resp = self.branch_api.get_branch(owner=USERNAME, repo=repo_name, branch=branch_name)
        assert get_branch_resp.status_code == 404



