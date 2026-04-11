import time
import pytest
from api import RepositoryApi, GitHubClient, BranchApi, PullRequestApi, ContentApi
from models.branch_test_data.branch_test_data import CreateBranchTestData
from test_data import UserTestData



@pytest.fixture(scope='class', autouse=True)
def create_temporary_repo(request):
    # Check for a custom marker on the class
    # Default: No README
    with_readme = False

    # Look for @pytest.mark.repo_config(with_readme=True)
    marker = request.node.get_closest_marker("repo_config")
    if marker:
        with_readme = marker.kwargs.get("with_readme", False)

    # Prepare the payload
    repository_name = f"tmp-repo-{int(time.time())}"
    payload = {
        "name": repository_name,
        "description": "Temp repo for E2E tests",
        "private": False,
        "auto_init": with_readme
    }

    # Create the repo
    client = GitHubClient(UserTestData.base_url, UserTestData.token)
    repo_api = RepositoryApi(client)
    repo_api.create_repo_for_authenticated_user(payload)

    # Provide data to the test class
    # We attach it to the class instance so tests can access self.repo_name
    if request.cls is not None:
        request.cls.repo_name = repository_name

    yield repository_name  # The tests run here

    # TEARDOWN: Delete the repo after the class finishes
    user_name = UserTestData.user_name
    repo_api.delete_repo(owner=user_name, repo_name=repository_name)


@pytest.fixture(scope='class')
def temporary_branches_with_prs(create_temporary_repo, number_of_branches):
    repo_name = create_temporary_repo
    client = GitHubClient(UserTestData.base_url, UserTestData.token)
    branch_api = BranchApi(client)
    pr_api = PullRequestApi(client)  # Assuming you have a PR API class
    content_api = ContentApi(client)  # Needed to create a commit

    # 1. Get Base SHA
    sha_resp = branch_api.get_branch_sha(owner=UserTestData.user_name, repo=repo_name)
    sha_resp.raise_for_status()
    source_sha = sha_resp.json()["object"]["sha"]

    created_branches = []
    created_pr_numbers = []

    try:
        for i in range(number_of_branches):
            branch_name = f"feature-pr-{i}"

            # 2. Create the Branch
            branch_api.create_branch(
                owner=UserTestData.user_name,
                repo=repo_name,
                data={"ref": f"refs/heads/{branch_name}", "sha": source_sha}
            ).raise_for_status()

            # 3. Add a Commit (PRs require a difference between branches)
            content_api.create_file(
                owner=UserTestData.user_name,
                repo=repo_name,
                path=f"file_{i}.txt",
                message=f"Initial commit for {branch_name}",
                content=f"Unique content for branch {i}",
                branch=branch_name
            ).raise_for_status()

            # 4. Create the Pull Request
            pr_resp = pr_api.create_pull_request(
                owner=UserTestData.user_name,
                repo=repo_name,
                data={
                    "title": f"Pull Request for {branch_name}",
                    "head": branch_name,
                    "base": "main",
                    "body": "This is an automated test PR."
                }
            )
            pr_resp.raise_for_status()

            created_branches.append(branch_name)
            created_pr_numbers.append(pr_resp.json()["number"])

        yield created_branches, created_pr_numbers

    finally:
        # Cleanup: Deleting the branch automatically closes/cleans up the PR
        for branch in created_branches:
            branch_api.delete_branch(owner=UserTestData.user_name, repo=repo_name, branch_name=branch)


@pytest.fixture(scope='class')
def number_of_branches(request):
    """
    This is the missing link. It takes the value from the
    parametrize decorator and provides it to your other fixtures.
    """
    return request.param

