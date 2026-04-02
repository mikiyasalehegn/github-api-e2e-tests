import pytest
from api.issue_api import IssueApi
from base import BaseTest
from utils.config import USERNAME
from models import CreateIssuePayload, IssueResponseData, IssueTestData, create_issue_response_schema
import logging




logger = logging.getLogger(__name__)



@pytest.mark.userfixture("create_temporary_repo")
class TestIssueManagementFlow(BaseTest):
    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.issue_api = IssueApi(self.client)

    def test_create_issue(self, create_temporary_repo):
        issue_repo_name = create_temporary_repo
        # payload = CreateIssuePayload()
        response = self.issue_api.create_issue(owner=USERNAME, repo=issue_repo_name, data={})
