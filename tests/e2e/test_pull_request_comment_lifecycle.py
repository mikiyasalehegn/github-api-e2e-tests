import pytest
import logging
from api.commit_api import CommitApi
from base import BaseTest
from utils import USERNAME



logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("create_temporary_repo")
@pytest.mark.repo_config(with_readme=True)
class TestPullRequestCommentLifecycle(BaseTest):

    def setup_method(self):
        super().setup_method()

        self.client = self.get_client()
        self.commit_api = CommitApi(self.client)

    def test_pull_request_comment_lifecycle(self, create_temporary_repo):
        repo_name = create_temporary_repo

        # ----------------------- get commit ----------------
        list_commit_resp = self.commit_api.list_commits(owner=USERNAME, repo=repo_name)
        logger.info(f"list_commit_resp: {list_commit_resp.text}")
        list_commit_resp.status_code = 200
        target_commit = [data for data in list_commit_resp.json() if data["author"]["login"] == USERNAME]
        commit_sha = target_commit[0]["sha"]

        # ----------------------- create commit ----------------
        # owner, repo, commit_sha, content
        create_commit_resp = self.commit_api.create_commit_comment(owner=USERNAME, repo=repo_name,commit_sha=commit_sha,
                                                                   content="Create comment for a commit")
        logger.info(f"create_commit_resp: {create_commit_resp.text}")
        create_commit_resp.status_code = 201


