import pytest
import logging
from api.commit_api import CommitApi
from base import BaseTest
from test_data import PullRequestDataTest
from utils import USERNAME



logger = logging.getLogger(__name__)


@pytest.mark.usefixtures("feature_branch_ready_for_pr")
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

        # ----------------------- create commit comments----------------
        create_commit_comment = self.commit_api.create_commit_comment(owner=USERNAME, repo=repo_name,
                                                                      commit_sha=commit_sha,
                                                                      content={"body": PullRequestDataTest.default_commit_comment})
        logger.info(f"create_commit_comment: {create_commit_comment.text}")
        create_commit_comment.status_code = 201


        # ----------------------- create commit comments----------------
        get_commit_comment = self.commit_api.list_commit_comments(owner=USERNAME, repo=repo_name, commit_sha=commit_sha)
        logger.info(f"get_commit_comment: {get_commit_comment.text}")
        get_commit_comment.status_code = 200
        comment_id = [item["id"] for item in get_commit_comment.json() if item["user"]["login"] == USERNAME]

        # ----------------------- update commit comment ----------------
        update_commit_comment_resp = self.commit_api.update_commit_comment(owner=USERNAME, repo=repo_name,
                                                                           comment_id=comment_id[0],
                                                                           content={"body": PullRequestDataTest.updated_commit_comment})
        logger.info(f"update_commit_comment_resp: {update_commit_comment_resp.text}")
        update_commit_comment_resp.status_code = 200
        update_commit_comment_resp.json()["body"] = PullRequestDataTest.updated_commit_comment

        # ----------------------- delete commit comment ----------------
        delete_commit_comment_resp = self.commit_api.delete_commit_comment(owner=USERNAME, repo=repo_name,
                                                                      comment_id=comment_id[0])
        logger.info(f"delete_commit_comment: {delete_commit_comment_resp.text}")
        delete_commit_comment_resp.status_code = 204


        # ----------------------- verify commit comment is erased ----------------
        get_commit_comment_resp = self.commit_api.get_commit_comment(owner=USERNAME, repo=repo_name,
                                                                     comment_id=comment_id[0])
        logger.info(f"get_commit_comment_resp: {get_commit_comment_resp.text}")
        get_commit_comment_resp.status_code = 404


