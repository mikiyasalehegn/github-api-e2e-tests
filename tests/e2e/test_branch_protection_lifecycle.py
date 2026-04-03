import pytest
from api import BranchApi
from base import BaseTest
from utils import USERNAME, assert_data_schema
import time
import logging
from models import BranchTestData, update_branch_protection_schema, BranchTestResponse


logger = logging.getLogger(__name__)




@pytest.mark.usefixtures("create_temporary_repo")
@pytest.mark.repo_config(with_readme=True)
class TestBranchProtectionLifecycle(BaseTest):

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.branch_api = BranchApi(self.client)

    def test_branch_protection_lifecycle(self, create_temporary_repo):

        # -------------------- Get Source SHA from Main --------------------
        branch_temp_repo = create_temporary_repo
        time.sleep(2)
        sha_resp = self.branch_api.get_branch_sha(owner=USERNAME, repo=branch_temp_repo)
        logger.info(f"sha_resp data: {sha_resp.text}")
        assert sha_resp.status_code == 200


        # -------------------- Update Branch Protection --------------------
        payload = BranchTestData()
        update_protection_resp = self.branch_api.update_branch_protection(owner=USERNAME, repo=branch_temp_repo,
                                                                     data=payload.to_dict())
        assert_branch_protection = BranchTestResponse(update_protection_resp.json())
        logger.info(f"update_protection data: {update_protection_resp.text}")
        assert update_protection_resp.status_code == 200
        assert_data_schema(update_protection_resp, update_branch_protection_schema)
        assert assert_branch_protection.required_pull_request_reviews["required_approving_review_count"] == 1
        assert assert_branch_protection.enforce_admins["enabled"] == True
        assert assert_branch_protection.allow_force_pushes["enabled"] == True
        assert assert_branch_protection.allow_deletions["enabled"] == True



