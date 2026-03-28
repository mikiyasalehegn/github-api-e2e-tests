from api import GitHubClient
import os
import pytest
from dotenv import load_dotenv

load_dotenv()


class BaseTest:

    def setup_method(self):
        self.base_url = os.getenv("BASE_URL")
        self.default_token = os.getenv("TOKEN")

    def get_client(self, token=None):
        """Factory method to create client with any token"""
        return GitHubClient(
            self.base_url,
            token if token else self.default_token
        )