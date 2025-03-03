from .messages import messages
from .dbs.database import db
from .keyboard.kb_builder import get_stats,prelink,cancel
import os
from dotenv import load_dotenv
load_dotenv()

waiting_for_message = {}
TOKEN = os.getenv('BOT_TOKEN')