import pytest
from api import BranchApi
from base import BaseTest
from test_data import UserTestData
import logging

from utils import USERNAME

logger = logging.getLogger(__name__)


@pytest.mark.repo_config(with_readme=True)
class TestStaleResourceCleanupLogic(BaseTest):

    def setup_method(self):
        super().setup_method()
        self.client = self.get_client()
        self.branch_api = BranchApi(self.client)

    @pytest.mark.parametrize("number_of_branches", [3], indirect=True)
    def test_stale_resource_cleanup_logic(self, number_of_branches, temporary_branches, create_temporary_repo):
        branches = temporary_branches
        repo_name = create_temporary_repo

        # ------------------- Make sure the branch is created -------------------

        get_branches = self.branch_api.list_branches(owner=UserTestData.user_name, repo=repo_name)
        logger.info(f"get_branches: {get_branches.text}")
        branch_names = [x["name"] for x in get_branches.json()]
        assert set(branches).issubset(set(branch_names))

        # ------------------- Merge the first two branches -------------------
        for index, branch in enumerate(branches[0: 1]):
            merge_branch_resp = self.branch_api.merge_branch(owner=USERNAME, repo=repo_name, data={
                "base": "main", "head": branches[index], "commit_message": "test merge branch",
            })
            logger.info(f"merge_branch_resp data: {merge_branch_resp.text}")
            assert merge_branch_resp.status_code == 204

        # ------------------- Verify the merged and unmerged branches -------------------
        filter_merged_branches = self.branch_api.filter_branch(owner=UserTestData.user_name, repo=repo_name, state="closed")
        logger.info(f"filter_merged_branches: {filter_merged_branches.text}")
        assert filter_merged_branches.status_code == 200





