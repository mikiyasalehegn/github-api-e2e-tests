import pytest
from api import PullRequestApi, BranchApi, PrCommentApi
from base import BaseTest
from utils import USERNAME
import logging


logger = logging.getLogger(__name__)


@pytest.mark.repo_config(with_readme=True)
class TestNegativeCommentOnDeleteBranchPr(BaseTest):

    def setup_method(self):
        super().setup_method()

        client = self.get_client()
        self.pr_api = PullRequestApi(client)
        self.branch_api = BranchApi(client)
        self.pr_comment_api = PrCommentApi(client)

    @pytest.mark.parametrize("temporary_branches_with_prs", [{"count": 1, "is_draft": False}], indirect=True)
    def test_negative_comment_on_deleted_branch_pr(self, create_temporary_repo, temporary_branches_with_prs):
        repo_name = create_temporary_repo
        branches, pr_numbers = temporary_branches_with_prs

        # ------------------------ get_commit_sha ------------------------
        get_pr_resp = self.pr_api.get_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_numbers[0])
        commit_sha = get_pr_resp.json()["head"]["sha"]

        # ------------------------ delete branch ------------------------
        delete_branch_resp = self.branch_api.delete_branch(owner=USERNAME, repo=repo_name, branch_name=branches[0])
        delete_branch_resp.status_code = 204

        # ------------------------ add comment to the pr ------------------------
        payload = {
            "body": "This is a test comment",
            "commit_id": commit_sha, # Must be the latest SHA in the PR
            "path": "README.md",
            "start_side": 'RIGHT',
            "line": 1,
            "side": 'RIGHT'
        }

        add_pr_review_comment = self.pr_comment_api.create_pr_review_comment(owner=USERNAME,repo=repo_name,
                                                                             pr_number=pr_numbers[0], data=payload)
        logger.info(f"add_pr_review_comment: {add_pr_review_comment.text}")
        assert add_pr_review_comment.status_code == 422
        assert "Validation Failed" in add_pr_review_comment.json()["message"]
        assert "pull_request_review_thread.path" in add_pr_review_comment.json()["errors"][0]["field"] # make sure the api couldn't find the path
