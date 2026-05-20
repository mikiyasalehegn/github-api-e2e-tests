import time
import pytest
from api import PullRequestApi, BranchApi, ContentApi
from base import BaseTest
from models import CreateBranchTestData
from test_data import PullRequestDataTest
from utils import USERNAME
from models import CreatePrPayload
import logging


logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("create_temporary_repo")
@pytest.mark.repo_config(with_readme=True)
class TestBranchDeletionClosesAssociatedPRs(BaseTest):
    def setup_method(self):
        super().setup_method()

        client = self.get_client()
        self.pr_api = PullRequestApi(client)
        self.branch_api = BranchApi(client)
        self.content_api = ContentApi(client)

    def test_branch_deletion_closes_associated_prs(self, create_temporary_repo):
        repo_name = create_temporary_repo
        branch_name = "feature-branch"
        sha_resp = self.branch_api.get_branch_sha(owner=USERNAME, repo=repo_name)
        assert sha_resp.status_code == 200
        source_sha = sha_resp.json()["object"]["sha"]


        # ------------------------ create branch ------------------------
        payload = CreateBranchTestData(name=branch_name, source_sha=source_sha)
        create_branch_resp = self.branch_api.create_branch(owner=USERNAME, repo=repo_name, data=payload.to_dict())
        logger.info(f"create_branch_resp data: {create_branch_resp.text}")

        # ------------------------- update readme on feature-branch -------------------------
        content_a = f"Change on {branch_name}"
        update_readme_branch_a = self.content_api.update_repo_file(owner=USERNAME, repo=repo_name,
                                                                         new_line_content=content_a, path="README.md",
                                                                         branch=branch_name)
        logger.info(f"update_readme_branch_a data: {update_readme_branch_a.text}")
        assert update_readme_branch_a.status_code == 200

        # ------------------------- create pr for the -------------------------
        payload = CreatePrPayload(title=PullRequestDataTest.closed_pr_title, head=branch_name, base="main",
                                  body=PullRequestDataTest.pr_body)
        pr_response = self.pr_api.create_pull_request(owner=USERNAME, repo=repo_name, data=payload.to_dict())
        logger.info(f"pr_response data: {pr_response.text}")
        pr_response.status_code = 201

        # ------------------------- delete the branch -------------------------
        delete_branch_resp = self.branch_api.delete_branch(owner=USERNAME, repo=repo_name, branch_name=branch_name)
        logger.info(f"delete_branch_resp data: {delete_branch_resp.text}")
        assert delete_branch_resp.status_code == 204
        pr_number = pr_response.json()["number"]
        time.sleep(1)

        # ------------------------- get pull request -------------------------
        get_pr_resp = self.pr_api.get_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_number)
        logger.info(f"get_pr_resp data: {get_pr_resp.text}")
        assert get_pr_resp.status_code == 200
        assert get_pr_resp.json()["state"] == "closed"
