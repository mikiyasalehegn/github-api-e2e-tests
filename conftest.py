import pytest
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def token():
    return os.getenv("GITHUB_TOKEN")