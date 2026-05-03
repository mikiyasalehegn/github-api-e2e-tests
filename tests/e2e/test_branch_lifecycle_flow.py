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

    def check_the_branch_exists(self, owner, repo, branch):
        get_branch_resp = self.branch_api.get_branch(owner=owner, repo=repo,
                                                     branch=branch)
        logger.info(f"get_branch_resp data: {get_branch_resp.text}")

        return get_branch_resp

    def test_branch_lifecycle_flow(self, create_temporary_repo):

        # -------------------- Get Source SHA from Main --------------------
        branch_temp_repo = create_temporary_repo
        time.sleep(2)
        sha_resp = self.branch_api.get_branch_sha(owner=USERNAME, repo=branch_temp_repo)
        logger.info(f"sha_resp data: {sha_resp.text}")
        assert sha_resp.status_code == 200
        source_sha = sha_resp.json()["object"]["sha"]

        # -------------------- Create Branch from Main --------------------
        payload = CreateBranchTestData(name=BranchTestData.branch_name, source_sha=source_sha)
        create_branch_resp = self.branch_api.create_branch(owner=USERNAME, repo=branch_temp_repo, data=payload.to_dict())
        logger.info(f"create_branch_resp data: {create_branch_resp.text}")
        assert create_branch_resp.status_code == 201
        assert create_branch_resp.json()["object"]["sha"] == source_sha


        # -------------------- Rename Branch --------------------
        rename_branch_resp = self.branch_api.rename_branch(owner=USERNAME, repo=branch_temp_repo,
                                                           branch=BranchTestData.branch_name,
                                                           data={"new_name": BranchTestData.new_branch_name})
        logger.info(f"rename_branch_resp data: {rename_branch_resp.text}")
        assert rename_branch_resp.status_code == 201
        assert rename_branch_resp.json()["name"] == BranchTestData.new_branch_name


        # -------------------- Get Branch --------------------
        get_branch_resp = self.check_the_branch_exists(owner=USERNAME, repo=branch_temp_repo,
                                                       branch=BranchTestData.new_branch_name)
        assert get_branch_resp.json()["name"] == BranchTestData.new_branch_name


        # -------------------- Merge Branch --------------------
        merge_branch_resp = self.branch_api.merge_branch(owner=USERNAME, repo=branch_temp_repo, data={
            "base": "main", "head": BranchTestData.new_branch_name, "commit_message": BranchTestData.commit_message
        })
        logger.info(f"merge_branch_resp data: {merge_branch_resp.text}")
        assert merge_branch_resp.status_code == 204


        # -------------------- Delete Branch --------------------
        delete_branch_resp = self.branch_api.delete_branch(owner=USERNAME, repo=branch_temp_repo,
                                                           branch_name=BranchTestData.new_branch_name)
        assert delete_branch_resp.status_code == 204

        # -------------------- Check a branch is erased --------------------
        get_branch_resp = self.check_the_branch_exists(owner=USERNAME, repo=branch_temp_repo,
                                                       branch=BranchTestData.new_branch_name)
        assert get_branch_resp.status_code == 404





