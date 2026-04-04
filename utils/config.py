import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
COLLABORATOR = os.getenv("COLLABORATOR")
COLLABORATOR_TOKEN = os.getenv("COLLABORATOR_TOKEN")