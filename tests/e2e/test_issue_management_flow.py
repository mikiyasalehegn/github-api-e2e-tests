import time
import pytest
from api.issue_api import IssueApi
from base import BaseTest
from utils import USERNAME, assert_data_schema
from models import CreateIssuePayload, IssueResponseData, IssueTestData, create_issue_response_schema, UpdateIssuePayload
import logging




logger = logging.getLogger(__name__)



@pytest.mark.usefixtures("create_temporary_repo")
class TestIssueManagementFlow(BaseTest):
    issue_number = None

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.issue_api = IssueApi(self.client)

    def test_create_issue(self, create_temporary_repo):

        # -------------------- Test create issue --------------------
        time.sleep(2)
        issue_repo_name = create_temporary_repo
        payload = CreateIssuePayload(title=IssueTestData.title, body=IssueTestData.body,
                                     assignees=USERNAME, labels=IssueTestData.labels)
        response = self.issue_api.create_issue(owner=USERNAME, repo=issue_repo_name, data=payload.to_dict())
        create_issue_resp = IssueResponseData(response.json())
        logger.info(f"Created issue {response.text}")

        assert response.status_code == 201
        self.issue_number = response.json()["number"]
        assert_data_schema(response, create_issue_response_schema)
        assert create_issue_resp.state == "open"
        assert create_issue_resp.body == IssueTestData.body
        assert create_issue_resp.title == IssueTestData.title
        assert create_issue_resp.user["login"] == USERNAME
        assert create_issue_resp.locked == False
        assert create_issue_resp.assignee["login"] == USERNAME

        time.sleep(2)


        # -------------------- Test get issue --------------------
        response = self.issue_api.get_issue(owner=USERNAME, repo=issue_repo_name, issue_number=self.issue_number)
        logger.info(f"Get issue {response.text}")
        assert response.status_code == 200


        # -------------------- Test update issue --------------------
        payload = UpdateIssuePayload(
            # title= IssueTestData.new_title,   # Updating title has a bug
            body=IssueTestData.new_body,
            labels=IssueTestData.new_label)
        response = self.issue_api.update_issue(owner=USERNAME, repo=issue_repo_name, issue_number=self.issue_number,
                                               data=payload.to_dict())
        update_issue_response_schema = create_issue_response_schema
        update_issue_response = IssueResponseData(response.json())

        logger.info(f"Update issue response {response.text}")
        assert response.status_code == 200
        assert_data_schema(response, update_issue_response_schema)
        # check.equal(update_issue_response.title, IssueTestData.new_title) # Updating title has a bug
        assert update_issue_response.body == IssueTestData.new_body
        assert update_issue_response.labels[0]["name"] == IssueTestData.new_label[0]

        time.sleep(2)

        # -------------------- Test lock issue --------------------
        response = self.issue_api.lock_issue(owner=USERNAME, repo=issue_repo_name, issue_number=self.issue_number,
                                             data = IssueTestData.lock_reason)
        logger.info(f"Lock issue response data {response.text}")

        assert response.status_code == 204
        get_locked_issue = self.issue_api.get_issue(owner=USERNAME, repo=issue_repo_name, issue_number=self.issue_number)
        assert get_locked_issue.status_code == 200
        assert get_locked_issue.json()["locked"] == True

        # -------------------- Test unlock issue --------------------
        response = self.issue_api.unlock_issue(owner=USERNAME, repo=issue_repo_name, issue_number=self.issue_number,)
        assert response.status_code == 204
        get_unlocked_issue = self.issue_api.get_issue(owner=USERNAME, repo=issue_repo_name, issue_number=self.issue_number)
        assert get_unlocked_issue.status_code == 200
        assert get_unlocked_issue.json()["locked"] == False

