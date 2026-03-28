import os
from dotenv import load_dotenv

load_dotenv()


class UserTestData:
    user_name = os.getenv("USERNAME")
    new_user_name = "New User"
    user_type = "User"
    twitter_username = "Twitter Username"
    bio= "I am QA Automation Engineer"
    original_twitter_username = None
    original_bio = None
