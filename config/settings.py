import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8080")
GITHUB_API = os.getenv("GITHUB_API")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ADMIN_USER: str = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin")
DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "false"
SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
