from api import GitHubClient
from utils.config import BASE_URL, TOKEN


class BaseTest:

    def setup_method(self):
        self.base_url = BASE_URL
        self.default_token = TOKEN

    def get_client(self, token=None):
        """Factory method to create client with any token"""
        return GitHubClient(
            self.base_url,
            token if token else self.default_token
        )