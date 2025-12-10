from dotenv import load_dotenv
import os


load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '1240841018'))
DB_PATH = os.getenv('DATABASE_PATH', './data/bot.db')
RATE_LIMIT_PER_HOUR = int(os.getenv('RATE_LIMIT_PER_HOUR', '3'))
SCREENSHOT_API_KEY = os.getenv('SCREENSHOT_API_KEY')
ALLOW_PUBLIC_SCREENSHOT = os.getenv('ALLOW_PUBLIC_SCREENSHOT', 'false').lower() in ('1','true')


# Forbidden patterns
FORBIDDEN_DOMAINS = ['.gov', '.mil']