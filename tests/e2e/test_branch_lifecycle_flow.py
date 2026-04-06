import time
import pytest
import logging
from api import BranchApi
from base import BaseTest
from models.branch_test_data.branch_test_data import BranchTestData, CreateBranchTestData
from utils import USERNAME

logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("create_temporary_repo")
@pytest.mark.repo_config(with_readme=True)
class TestBranchLifecycleFlow(BaseTest):

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.branch_api = BranchApi(self.client)

    def test_branch_lifecycle_flow(self, create_temporary_repo):

        # -------------------- Get Source SHA from Main --------------------
        branch_temp_repo = create_temporary_repo
        time.sleep(2)
        sha_resp = self.branch_api.get_branch_sha(owner=USERNAME, repo=branch_temp_repo)
        logger.info(f"sha_resp data: {sha_resp.text}")
        assert sha_resp.status_code == 200
        source_sha = sha_resp.json()["object"]["sha"]






