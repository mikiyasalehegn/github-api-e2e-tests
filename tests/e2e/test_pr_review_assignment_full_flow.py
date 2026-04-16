import pytest
from base import BaseTest
from api import PullRequestReviewAPI, RepoCollabApi, InvitationApi
from test_data import UserTestData
import logging
from utils import USERNAME, COLLABORATOR, COLLABORATOR_TOKEN


logger = logging.getLogger(__name__)


@pytest.mark.repo_config(with_readme=True)
class TestPRReviewAssignmentFullFlow(BaseTest):

    def setup_method(self):
        super().setup_method()

        client = self.get_client()
        self.pr_review_api = PullRequestReviewAPI(client)
        self.repo_collab_api = RepoCollabApi(client)

    def get_pr_review(self, owner, repo_name, pr_numbers):
        get_pr_review_response = self.pr_review_api.get_pr_review_request(owner=owner, repo=repo_name,
                                                                          pr_number=pr_numbers)
        return get_pr_review_response

    @pytest.mark.parametrize("temporary_branches_with_prs", [{"count": 1, "is_draft": False}], indirect=True)
    def test_pr_review_assignment_full_flow(self, temporary_branches_with_prs, create_temporary_repo):
        branches, pr_numbers = temporary_branches_with_prs
        repo_name = create_temporary_repo

        # ------------------- add collaborator -------------------
        add_repo_collab_response = self.repo_collab_api.add_repo_collaborator(owner=USERNAME, repo=repo_name,
                                                                              username=COLLABORATOR)
        logger.info(f"add_repo_collaborator response: {add_repo_collab_response.text}")
        assert add_repo_collab_response.status_code == 201
        invitation_id = add_repo_collab_response.json()["id"]

        # ------------------- accept repo collab invitation -------------------
        invitation_client = self.get_client(token=COLLABORATOR_TOKEN)
        accept_invitation_api = InvitationApi(invitation_client)
        accept_invitation_response = accept_invitation_api.accept_invitation(invitation_id=invitation_id)
        logger.info(f"accept_invitation response: {accept_invitation_response.text}")

        # ------------------- request pr review -------------------
        request_review_response = self.pr_review_api.request_pr_review(owner=UserTestData.user_name, repo=repo_name,
                                                                       pr_number=pr_numbers[0],
                                                                       data={"reviewers": [COLLABORATOR]})
        logger.info(f"request_review_response: {request_review_response.text}")
        assert request_review_response.status_code == 201
        assert request_review_response.json()["requested_reviewers"][0]["login"] == COLLABORATOR

        # ------------------- verify the review request -------------------
        verify_pr_review = self.get_pr_review(owner=USERNAME, repo_name=repo_name, pr_numbers=pr_numbers[0])
        logger.info(f"verify_pr_review: {verify_pr_review.text}")
        assert verify_pr_review.status_code == 200
        assert verify_pr_review.json()["users"][0]["login"] == COLLABORATOR

        # ------------------- remove the review request -------------------
        remove_review_request_resp = self.pr_review_api.remove_pr_review(owner=UserTestData.user_name, repo=repo_name,
                                                                         pr_number=pr_numbers[0],
                                                                         data={"reviewers": [COLLABORATOR]})
        logger.info(f"remove_review_request_response: {remove_review_request_resp.text}")
        remove_review_request_resp.status_code = 200

        # ------------------- verify the review request is removed -------------------
        verify_pr_review = self.get_pr_review(owner=USERNAME, repo_name=repo_name, pr_numbers=pr_numbers[0])
        logger.info(f"verify_pr_review is removed: {verify_pr_review.text}")
        assert verify_pr_review.status_code == 200
        assert verify_pr_review.json()["users"] == []
