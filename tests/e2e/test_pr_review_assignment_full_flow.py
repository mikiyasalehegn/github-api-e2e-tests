import pytest
from base import BaseTest
from api import PullRequestReviewAPI
from test_data import UserTestData
import logging


logger = logging.getLogger(__name__)


@pytest.mark.repo_config(with_readme=True)
class TestPRReviewAssignmentFullFlow(BaseTest):

    def setup_method(self):
        super().setup_method()

        client = self.get_client()
        self.pr_review_api = PullRequestReviewAPI(client)

    @pytest.mark.parametrize("number_of_branches", [1], indirect=True)
    def test_pr_review_assignment_full_flow(self, number_of_branches, temporary_branches_with_prs, create_temporary_repo):
        branches, pr_numbers = temporary_branches_with_prs
        repo_name = create_temporary_repo

        # ------------------- get pr review -------------------
        get_pr_review_response = self.pr_review_api.get_pr_review_request(owner=UserTestData.user_name, repo=repo_name,
                                                                          pr_number=pr_numbers[0])
        logger.info(f"get_pr_review_response: {get_pr_review_response.text}")
        get_pr_review_response.status_code = 200


        # ------------------- request pr review -------------------
        # request_review_response = self.pr_review_api.get_pr_review_request(owner=UserTestData.user_name, repo=repo_name,
        #                                                                    pr_number=pr_numbers[0])
        # logger.info(f"request_review_response: {request_review_response.text}")
        # assert get_pr_review_response.status_code == 200





