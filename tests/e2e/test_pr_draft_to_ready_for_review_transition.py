import pytest
from api import PullRequestApi
from base import BaseTest
from conftest import create_temporary_repo
from utils import USERNAME
import logging


logger = logging.getLogger(__name__)


@pytest.mark.repo_config(with_readme=True)
class TestPRDraftToReadyForReviewTransition(BaseTest):
    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.pr_api = PullRequestApi(self.client)

    @pytest.mark.parametrize("temporary_branches_with_prs", [{"count": 1, "is_draft": True}], indirect=True)
    def test_pr_draft_to_ready_for_review_transition(self, create_temporary_repo, temporary_branches_with_prs):
        repo_name = create_temporary_repo
        branches, pr_numbers = temporary_branches_with_prs

        # ------------------------ get the pr ------------------------
        get_pr_resp = self.pr_api.get_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_numbers[0])
        logger.info(f"get_pr_resp: {get_pr_resp.text}")
        assert get_pr_resp.status_code == 200
        assert get_pr_resp.json()["draft"] == True

        # ------------------------ try to merge the pr ------------------------
        merge_pr_resp = self.pr_api.merge_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_numbers[0])
        assert merge_pr_resp.status_code in [422, 405]

        # ------------------------ make the pr ready for review ------------------------
        payload = {"draft": False}
        update_pr_resp = self.pr_api.update_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_numbers[0],
                                                         data=payload)
        logger.info(f"update_pr_resp: {update_pr_resp.text}")
        assert update_pr_resp.status_code == 200

        # ------------------------ get the pr ------------------------
        get_pr_resp = self.pr_api.get_pull_request(owner=USERNAME, repo=repo_name, pr_number=pr_numbers[0])
        logger.info(f"get_pr_resp: {get_pr_resp.text}")
        assert get_pr_resp.status_code == 200
        assert get_pr_resp.json()["draft"] == False #This is a bug





