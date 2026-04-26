import time
import pytest
from api import PullRequestApi, BranchApi, ContentApi
from base import BaseTest
from models.branch_test_data.branch_test_data import CreateBranchTestData, BranchTestData
from test_data import PullRequestDataTest
from utils import USERNAME
import logging

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("create_temporary_repo")
@pytest.mark.repo_config(with_readme=True)
class TestPRMergeConflictDetection(BaseTest):
    def setup_method(self):
        super().setup_method()
        self.client = self.get_client()
        self.pr_api = PullRequestApi(self.client)
        self.branch_api = BranchApi(self.client)
        self.content_api = ContentApi(self.client)

    def test_merge_conflict_detection(self, create_temporary_repo):
        time.sleep(2)
        repo_name = create_temporary_repo
        sha_resp = self.branch_api.get_branch_sha(owner=USERNAME, repo=repo_name)
        logger.info(f"sha_resp data: {sha_resp.text}")
        assert sha_resp.status_code == 200
        source_sha = sha_resp.json()["object"]["sha"]

        # ------------------------- create two branches -------------------------
        payload = CreateBranchTestData(name="branch_a", source_sha=source_sha)
        branch_a_repo = self.branch_api.create_branch(owner=USERNAME, repo=repo_name, data=payload.to_dict())
        logger.info(f"branch_a_repo data: {branch_a_repo.text}")
        assert branch_a_repo.status_code == 201

        payload_b = CreateBranchTestData(name="branch_b", source_sha=source_sha)
        branch_b_repo = self.branch_api.create_branch(owner=USERNAME, repo=repo_name, data=payload_b.to_dict())
        logger.info(f"branch_b_repo data: {branch_b_repo.text}")
        assert branch_b_repo.status_code == 201

        # ------------------------- update readme on branch_a -------------------------
        content_a = "Change on branch_a"
        update_readme_branch_a = self.content_api.update_repo_file(owner=USERNAME, repo=repo_name,
                                                                         new_line_content=content_a, path="README.md",
                                                                         branch="branch_a")
        logger.info(f"update_readme_branch_a data: {update_readme_branch_a.text}")
        assert update_readme_branch_a.status_code == 200

        # ------------------------- update readme on branch_b -------------------------
        content_b = "Change on branch_b"
        update_readme_branch_b = self.content_api.update_repo_file(owner=USERNAME, repo=repo_name,
                                                                         new_line_content=content_b, path="README.md",
                                                                         branch="branch_b")
        logger.info(f"update_readme_branch_a data: {update_readme_branch_b.text}")
        assert update_readme_branch_a.status_code == 200

        # ------------------------- merge branch_a to main -------------------------
        payload = {
            "base": "main", "head": "branch_a", "commit_message": "merging branch_a into main"
        }
        merge_branch_a_resp = self.branch_api.merge_branch(owner=USERNAME, repo=repo_name, data=payload)
        logger.info(f"merge_branch_a_resp data: {merge_branch_a_resp.text}")

        # ------------------------- create pr for branch_b -------------------------
        payload = {
                    "title": "Pull request merge conflict",
                    "head": "branch_b",
                    "base": "main",
                    "body": PullRequestDataTest.pr_body
                }
        pr_response = self.pr_api.create_pull_request(owner=USERNAME, repo=repo_name, data=payload)
        logger.info(f"pr_response data: {pr_response.text}")
        pr_response.status_code = 201
        pr_number = pr_response.json()["number"]

        # ---------------------- Merge pr ------------------
        merge_pr_resp = self.pr_api.merge_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_number)
        logger.info(f"merge_pr_resp data: {merge_pr_resp.text}")
        assert merge_pr_resp.status_code == 405
        assert merge_pr_resp.json()["message"] == "Pull Request has merge conflicts"


