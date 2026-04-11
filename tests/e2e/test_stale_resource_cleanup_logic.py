import time
import pytest
from api import BranchApi, PullRequestApi
from base import BaseTest
from test_data import UserTestData
import logging



logger = logging.getLogger(__name__)


@pytest.mark.repo_config(with_readme=True)
class TestStaleResourceCleanupLogic(BaseTest):

    def setup_method(self):
        super().setup_method()
        self.client = self.get_client()
        self.branch_api = BranchApi(self.client)
        self.pr_api = PullRequestApi(self.client)

    @pytest.mark.parametrize("number_of_branches", [3], indirect=True)
    def test_stale_resource_cleanup_logic(self, number_of_branches, temporary_branches_with_prs, create_temporary_repo):
        branches, pr_numbers = temporary_branches_with_prs
        repo_name = create_temporary_repo

        # ------------------- Make sure the branch is created -------------------

        get_branches = self.branch_api.list_branches(owner=UserTestData.user_name, repo=repo_name)
        logger.info(f"get_branches: {get_branches.text}")
        branch_names = [x["name"] for x in get_branches.json()]
        assert set(branches).issubset(set(branch_names))

        # ------------------- Merge the first two branches -------------------
        for index, pr_num in enumerate(pr_numbers[0: 2]):
            merge_pr_resp = self.pr_api.merge_pull_request(owner=UserTestData.user_name, repo=repo_name, pr_number=pr_num)
            logger.info(f"merge_pr_resp data: {merge_pr_resp.text}")
            assert merge_pr_resp.status_code == 200

            time.sleep(1)
        # ------------------- Verify prs are merged -------------------
            get_merged_pr = self.pr_api.get_merged_pull_request(owner=UserTestData.user_name,
                                                                repo=repo_name, pr_number=pr_num)
            assert get_merged_pr.status_code == 204

        # ------------------- Verify the last pr is not merged -------------------
        unmerged_pr_resp = self.pr_api.get_pull_request(owner=UserTestData.user_name, repo=repo_name,
                                                        pr_number=pr_numbers[-1])
        assert unmerged_pr_resp.status_code == 200
        assert unmerged_pr_resp.json()["merged"] == False
