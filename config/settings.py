import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8080")
GITHUB_API = os.getenv("GITHUB_API")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# Optional: a token scoped without Administration write permission on the
# target repository, used to test authorization failures.
GITHUB_LOW_PRIVILEGE_TOKEN = os.getenv("GITHUB_LOW_PRIVILEGE_TOKEN")
# Optional: an organization (and a token for a non-owner member of it) used
# to test organization-level authorization scenarios.
GITHUB_ORG = os.getenv("GITHUB_ORG")
GITHUB_ORG_MEMBER_TOKEN = os.getenv("GITHUB_ORG_MEMBER_TOKEN")
ADMIN_USER: str = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin")
DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "false"
SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
