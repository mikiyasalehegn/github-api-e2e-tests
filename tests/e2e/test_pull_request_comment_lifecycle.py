import pytest
import logging
from api.commit_api import CommitApi
from base import BaseTest
from utils import USERNAME



logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("feature_branch_ready_for_pr")
@pytest.mark.repo_config(with_readme=True)
class TestPullRequestCommentLifecycle(BaseTest):

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.commit_api = CommitApi(self.client)

    @pytest.mark.parametrize("number_of_branches", [1], indirect=True)
    def test_pull_request_comment_lifecycle(self, number_of_branches, temporary_branches_with_prs, create_temporary_repo):
        branches, pr_number = temporary_branches_with_prs
        repo_name = create_temporary_repo



