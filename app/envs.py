from app.utils import get_env_var
from dotenv import load_dotenv
load_dotenv()

ADMIN_ID = int(get_env_var("ADMIN_ID"))
BOT_TOKEN = get_env_var("BOT_TOKEN")
DELAY_REQUESTS = int(get_env_var("DELAY_REQUESTS"))
TIMEOUT_REQUESTS = int(get_env_var("TIMEOUT_REQUESTS"))
DELAY_NOTIFY_CHECK = int(get_env_var("DELAY_NOTIFY_CHECK"))
CHECK_URL_BEFORE_NOTIFY = bool(get_env_var("CHECK_URL_BEFORE_NOTIFY"))
TIMEOUT_BEFORE_NOTIFY_REQUESTS = int(get_env_var("TIMEOUT_BEFORE_NOTIFY_REQUESTS"))
URLS_LIST = get_env_var("URLS")
