#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║             ⚡ 𝐀𝐍𝐎𝐒𝐱𝐆𝐎𝐃 ⚡                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  [REQUIRED PACKAGES]                                                 ║
║  >>> pip install python-telegram-bot                                 ║
║                                                                      ║
║  [HOW TO RUN]                                                        ║
║  1. pip install python-telegram-bot                                  ║
║  2. python 𝐀𝐍𝐎𝐒𝐱𝐆𝐎𝐃!!_bot_final.py                                        ║
║                                                                      ║
║  [FEATURES]                                                          ║
║  🚀 Multi-Bot Support (10 Bots)                                    ║
║  ⚡ Group Name Changing via Bots                                     ║
║  🛡️ Anti-Flood Protection                                          ║
║  🌪️ Multi-Threaded Spam/NC Engine                                  ║
║  🔒 Owner + Sudo System                                            ║
║  📝 Custom NC Lines & Slide Reply                                  ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import os
import sys
import time
import logging
import random
import re
import signal
import traceback
from collections import deque
from datetime import datetime, timedelta
from typing import Dict, Set, List, Optional, Tuple

from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatType, ParseMode
from telegram.error import RetryAfter, TimedOut, NetworkError, BadRequest, Forbidden
from telegram import Update

logging.basicConfig(
    format="%(asctime)s - [MULTI BOT] - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("MultiBot")

# ==================== CONFIGURATION ====================
OWNER_ID = 8697098817

# 10 Bot Tokens
BOT_TOKENS = [
    "7917451532:AAFMo4ociyOUKQHISfDDnZtRXlBCBrad004",
]

# Emoji lists
HEART_EMOJIS = ['🚗', '🏍️', '🚓', '🚙', '🚕', '🚘', '🚖', '🚌', '🚛', '🚜',
                '🐶', '🐱', '🐯', '🦁', '🐺', '🦊', '🐸', '🐵', '🐼', '🐨',
                '😀', '😈', '😂', '🤣', '😎', '😆', '😜', '😉', '😏', '😊',
                '🔥', '💥', '⚡', '🎯', '🎮', '🎲', '🏆', '📸', '🎧', '🧊']

FLAGS = ['🇮🇳ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇵🇰ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇧🇩ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇺🇸ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇬🇧ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇷🇺ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇨🇳ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇯🇵ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇰🇷ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇧🇷ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫',
         '🇩🇪ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇫🇷ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇮🇹ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇪🇸ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇨🇦ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇦🇺ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇮🇱ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇹🇷ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇸🇦ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫', '🇦🇪ｃｈｕｄ 𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫💠𒐫𒐫𒐫𒐫💠𒐫 𒐫𒐫𒐫']

HEARTS = ['❤️ 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '🧡 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💛 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💚 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💙 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💜 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '🖤 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '🤍 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '🤎 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💔 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', 
          '❣️ 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💕 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💞 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💓 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💗 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💖 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💘 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💝 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '💟 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)', '♥️ 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)']

UNAUTHORIZED_MESSAGE = "𝐒ꫝʏ 𝐀иꪮꜱ 𝐃ꫝꫝᴅʏ 𝐓ʜᴇɴ 𝐂ᴏᴍᴇ"

# ==================== USER'S CUSTOM NC LINES ====================
NC_LINES = [
    "{target} Tᴇʀɪ ᴍᴀᴀ ɢᴜʟᴀᴍ ʜ ʙᴇᴛᴇ🐣",
    "{target} Cᴜᴅ Cᴜᴅ Cᴜᴅ -!🩴🔥",
    "Aʟᴏᴏ Kʜᴀᴋᴇ {target} Tᴇʀɪ ᴍᴏᴍ Cᴏᴍ Qᴜᴇᴇɴ 👑♥️",
    "{target} Hɪᴊᴅᴀ Tᴇʀᴇ Bᴀᴀᴘ ᴋɪ Cʜᴜᴛ🤳🏻👋🏻",
    "{target} Tᴇʀᴇ Bᴀᴀᴘ Kɪ ʙᴋʙ🔥✨",
    "{target} Tᴜ ᴋʀᴇɢᴀ Sᴘᴀᴍ Hᴀssɪ🔃💠",
    "{target} Tᴇʀɪ Bʜᴇɴ Cʜᴏᴅᴇ Dɪɴᴀsᴀᴜʀ🦖😈",
    "{target} Aᴛᴍᴋʙғᴛᴊɢ🖤🙊",
    "{target} Kᴜᴛɪʏᴀ Kᴇ ʟᴀᴅᴋᴇ🌷😭",
    "{target} Tᴇʀᴀ ʙᴀᴀᴘ Tᴇʀɪ ᴍᴀᴀ ᴄʜᴏᴅᴇ Bʙᴄ Bᴀɴᴋᴇ😨♥️",
    "{target} Sɪʟᴀɪ Wᴀʟʏ ᴋᴇ ʟᴀᴅᴋᴇ Tʀʏ Mᴀᴀ ᴋᴀ ʙʜᴏsᴅᴀ Sɪʟ ᴅᴜ? 💀🥵",
    "{target} Tʀʏ ᴍᴀᴀ ᴘᴀᴅʜᴇ Bᴏᴏᴋ Wᴏʜ Hᴏᴋᴇ ᴄʜᴜᴅᴇɢɪ Cᴏᴏᴋ 🥧🧑🏻‍🍳",
    "{target} Eᴠᴇʀʏᴛʜɪɴɢ Is Tᴇᴍᴘᴏʀᴀʀʏ Bᴜᴛ Tʀɪ Cʜᴜᴅᴀɪ Is ᴘᴇʀᴍᴀɴᴇɴᴛ 🦠🦷",
    "{target} ᴋᴀʜᴀ ᴛᴇ ʙʜᴀɢᴇɢᴀ Eᴋ ʀᴇʜᴘᴀᴛ ᴍ ᴛᴇʀᴀ Rᴀᴘᴇ ʜᴏᴊʏᴇɢᴀ Bʜᴇɴɢᴇ🦘🪽",
    "{target} Tᴇʀɪ Mᴀᴀ ᴘᴇsᴇ ᴋᴀᴍᴀᴛᴇ ᴋᴀᴍᴀᴛᴇ ɴᴀɴɢɪ Hᴜɪ 👩🏻‍⚕️👩🏻‍🎤",
    "{target} Tᴇʀɪ ᴍᴀᴀ ᴋᴏ Mᴇʀᴇ FᴀʀᴍHᴏᴜsᴇ P ʙʜᴇᴊᴅᴇ🥩🍏",
    "{target} Kᴜᴛɪʏᴀ Kᴇ ʙʜᴏsᴅᴇ Kɪ ᴀᴜʟᴀᴅ😈👋🏻",
    "{target} ʙᴏʟᴇ 𝐀ɴᴏꜱ Kɪ ᴊᴀɪ Hᴏ🕳️🔥",
    "{target} ʜɪᴊᴅᴀ ʜ ᴛᴜ ɢʀᴇᴇʙ💮🥀",
    "{target} ᴛᴇʀɪ ᴍᴀᴀ ʙᴏʟᴇ 𝐏ʀ𝐎x𝐘 अब्बू ʜᴀɪ ᴍᴇʀᴇ🩴🔥"
]

# ==================== USER'S SLIDE LINES ====================
SLIDE_LINES = [
    "{target} ---PILLE Uth ",
    "{target} चुद गया tu-!",
    "Aʟᴏᴏ Kʜᴀᴋᴇ {target} Kɪ Mᴀ Cʜᴏᴅ Dᴜɴɢᴀ!",
    "{target} Cʜᴜᴅᴀ q chote🦖🪽",
    "{target} Bᴏʟᴇ 𝐀ɴᴏꜱ ᴘᴀᴘᴀ पिताश्री Mᴇʀɪ Mᴀ Cʜᴏᴅ Dᴏ",
    "{target} Kɪ Mᴀ Bᴏʟᴇ 𝐀ɴᴏꜱ ᴘᴀᴘᴀ Sᴇ Cʜᴜᴅᴜɴɢɪ",
    "{target} Kɪ Bᴇʜɴ Kɪ Cʜᴜᴛ Kᴀʟɪ Kᴀʟɪ",
    "{target} Kɪ Mᴀ Rᴀɴᴅɪ",
    "{target} ɢᴀʀᴇᴇʙ ᴋᴀ ʙᴀᴄʜʜᴀ",
    "{target} ᴄʜᴜᴅ ᴋᴇ ᴘᴀɢᴀʟ ʜᴏɢᴀʏᴀ",
    "{target} ᴋɪ ʙᴇʜɴ ᴄʜᴏᴅᴜ",
    "{target} ʟᴜɴᴅ ᴄʜᴜsᴇɢᴀ sᴀʙᴋᴀ",
    "{target} ᴋɪ ᴍᴀ ᴋᴏ ᴄʜᴏᴅᴇ 𝐀ɴᴏꜱ ᴘᴀᴘᴀ",
    "{target} ᴋɪ ᴍᴀ 𝐀ɴᴏꜱ ᴘᴀᴘᴀ ꜱᴇ ᴄʜᴜᴅᴇ",
    "{target} 𝐀ɴᴏꜱ ᴘᴀᴘᴀ ꜱᴇ ᴄʜᴜᴅᴀ",
    "{target} CUDKE MARGYA Tu",
    "{target} ɴᴇ 𝐀ɴᴏꜱ ᴘᴀᴘᴀ ᴋᴏ ʙᴀᴀᴩ ʙɴᴀ ʟɪyᴀ",
    "{target} ʙᴏʟᴇ 𝐀ɴᴏꜱ ᴘᴀᴘᴀ ᴩᴀᴩᴀ",
    "{target} ᴋɪ ᴀᴍᴍᴀ ᴄʜᴜᴅɪ",
    "{target} ᴋᴜᴛᴛᴇ sipahi polish kr 😋"
]

# Standard messages
NAME_CHANGE_MESSAGES = [
    "{target} 𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀),",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀) 💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀) 💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀) 💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀) 💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀) 💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀)💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀) 💢",
    "{target}  𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️??🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️𒈙🌌𒈙✨𒈙💎𒈙🦄𒈙🔮𒈙🕊️>>Sᴀʟᴀᴍ Tʜᴏᴋ ——➤(🎀) 💢",
]

REPLY_MESSAGES = [
    "{target} ᴛᴇʀɪ ᴍᴀᴀ ᴋᴏ ᴄʜᴏᴅᴜ 😈",
    "{target} ʀᴀɴᴅɪ ᴋᴇ ʙᴀᴄʜᴇ 💋",
    "{target} ᴛᴇʀɪ ʙᴇʜɴ ᴋɪ ᴄʜᴜᴛ 🍑",
    "{target} ɢᴀɴᴅᴜ ʙᴀᴄʜᴀ 😂",
    "{target} ᴛᴇʀɪ ᴍᴀᴀ ᴋᴀ ʙʜᴏꜱᴅᴀ 🌶️",
    "{target} ᴄʜᴜᴛɪʏᴀ ꜱᴀᴀʟᴀ 🤬",
    "{target} ʟᴜɴᴅ ᴋᴇ ʙᴀᴀʟ 🥜",
    "{target} ᴛᴇʀɪ ᴍᴀᴀ ꜱʜᴏʀᴇ ʜᴀɪ 🏖️",
    "{target} ʀᴀɴᴅɪ ᴋʜᴀɴᴇ ᴋᴀ ʙᴀᴄʜᴀ 🏠",
    "{target} ᴛᴇʀɪ ʙᴇʜɴ ᴋᴏ ɴᴀɴɢᴀ ᴋᴀʀᴜ 👙",
]

SPAM_MESSAGES = [
    "✝ 恐 𝐀𝐍𝐎𝐒!! ᴋɪ ᴊᴀɪ ʜᴏ {target} ᴋɪ ᴍᴀᴀ ᴄʜᴜᴅɪ ʙᴀᴅɪ 💗",
    "⚡ {target} ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴄʜᴜᴛ ᴍᴇɪɴ ʙᴏᴍʙ 💣",
    "🔥 {target} ɢᴀɴᴅᴜ ʙᴀᴄʜᴀ ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴄʜᴜᴛ 🍆",
    "🎯 {target} ᴛᴇʀɪ ʙᴇʜɴ ᴋᴏ ᴄʜᴏᴅᴜ ʙɪɴᴀ ᴄᴏɴᴅᴏᴍ 👅",
    "💀 {target} ᴛᴇʀɪ ᴍᴀᴀ ʀᴀɴᴅɪ ʙᴀᴢᴀᴀʀ ᴋɪ 🛒",
    "🐶 {target} ᴋᴜᴛᴛᴇ ᴋᴇ ᴘɪʟʟᴇ ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴄʜᴜᴛ 🦴",
    "⚔️ {target} ᴛᴇʀɪ ᴍᴀᴀ ᴋᴏ ꜱᴀʙ ᴄʜᴏᴅᴇɴɢᴇ 🗡️",
    "🚗 {target} ᴛᴇʀɪ ᴍᴀᴀ ᴋᴏ ɢᴀᴀᴅɪ ᴋᴇ ɴɪᴄʜᴇ ᴋᴜᴄʜʟᴜ 🚙",
]

# Settings
MAX_RETRIES = 3
BASE_RETRY_DELAY = 0.5
MAX_TASKS_PER_CHAT = 100
TASK_CLEANUP_INTERVAL = 30
CONNECTION_TIMEOUT = 30

# Global tracking
ALL_BOT_INSTANCES: Dict[int, 'BotInstance'] = {}
GLOBAL_STOP_EVENT = asyncio.Event()
COMMAND_LOCKS: Dict[int, asyncio.Lock] = {}
SUDO_USERS: Set[int] = set()

def get_command_lock(chat_id: int) -> asyncio.Lock:
    if chat_id not in COMMAND_LOCKS:
        COMMAND_LOCKS[chat_id] = asyncio.Lock()
    return COMMAND_LOCKS[chat_id]

class BotInstance:
    def __init__(self, bot_number: int, owner_id: int):
        self.bot_number = bot_number
        self.owner_id = owner_id
        self.authorized_users: Set[int] = set()
        self.active_spam_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_name_change_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_custom_nc_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_slide_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_reply_tasks: Dict[int, asyncio.Task] = {}
        self.active_reply_targets: Dict[int, str] = {}
        self.pending_replies: Dict[int, List[int]] = {}
        self.chat_delays: Dict[int, float] = {}
        self.chat_threads: Dict[int, int] = {}
        self.locks: Dict[int, asyncio.Lock] = {}
        self.stats = {"sent": 0, "errors": 0, "start_time": time.time(), "retries": 0, "rate_limits": 0}
        self.is_running = True
        self.last_cleanup = time.time()
        ALL_BOT_INSTANCES[bot_number] = self
        logger.info(f"Bot {bot_number} initialized")

    def get_lock(self, chat_id: int) -> asyncio.Lock:
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]

    def is_owner(self, user_id: int) -> bool:
        return user_id == self.owner_id

    def is_authorized(self, user_id: int) -> bool:
        return user_id == self.owner_id or user_id in self.authorized_users or user_id in SUDO_USERS

    async def check_owner(self, update: Update) -> bool:
        user_id = update.effective_user.id
        if not self.is_authorized(user_id):
            try:
                await update.message.reply_text(UNAUTHORIZED_MESSAGE)
            except Exception:
                pass
            return False
        return True

    async def check_main_owner(self, update: Update) -> bool:
        user_id = update.effective_user.id
        if not self.is_owner(user_id):
            try:
                await update.message.reply_text("⛔ Only main owner can use this!")
            except Exception:
                pass
            return False
        return True

    async def safe_cancel_tasks(self, tasks: List[asyncio.Task]):
        for task in tasks:
            if not task.done():
                task.cancel()
        for task in tasks:
            try:
                await asyncio.wait_for(asyncio.shield(task), timeout=2.0)
            except (asyncio.CancelledError, asyncio.TimeoutError, Exception):
                pass

    async def stop_all_tasks_globally(self) -> int:
        all_tasks = []

        for chat_id, tasks in list(self.active_spam_tasks.items()):
            all_tasks.extend(tasks)
            del self.active_spam_tasks[chat_id]

        for chat_id, tasks in list(self.active_name_change_tasks.items()):
            all_tasks.extend(tasks)
            del self.active_name_change_tasks[chat_id]

        for chat_id, tasks in list(self.active_custom_nc_tasks.items()):
            all_tasks.extend(tasks)
            del self.active_custom_nc_tasks[chat_id]

        for chat_id, tasks in list(self.active_slide_tasks.items()):
            all_tasks.extend(tasks)
            del self.active_slide_tasks[chat_id]

        for chat_id, task in list(self.active_reply_tasks.items()):
            all_tasks.append(task)
            del self.active_reply_tasks[chat_id]

        self.active_reply_targets.clear()
        self.pending_replies.clear()

        await self.safe_cancel_tasks(all_tasks)
        return len(all_tasks)

    # ==================== LOOPS ====================

    async def name_change_loop(self, chat_id: int, base_name: str, context: ContextTypes.DEFAULT_TYPE, worker_id: int = 1):
        """Standard name change loop"""
        msg_index = 0
        num_messages = len(NAME_CHANGE_MESSAGES)
        success_count = 0
        print(f"[Bot {self.bot_number}] NC Worker #{worker_id} STARTED for chat {chat_id}")

        while self.is_running and not GLOBAL_STOP_EVENT.is_set():
            try:
                delay = self.chat_delays.get(chat_id, 0)
                current_msg = NAME_CHANGE_MESSAGES[msg_index % num_messages]
                display_name = current_msg.format(target=base_name)

                try:
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name[:100])
                    msg_index += 1
                    success_count += 1
                    self.stats["sent"] += 1

                    if success_count % 50 == 0:
                        print(f"[Bot {self.bot_number}] NC #{worker_id}: {success_count} changes")

                    if delay > 0:
                        await asyncio.sleep(delay)

                except RetryAfter as e:
                    wait_time = e.retry_after
                    print(f"[Bot {self.bot_number}] Rate limited, waiting {wait_time}s")
                    await asyncio.sleep(wait_time + 0.5)

                except (TimedOut, NetworkError):
                    await asyncio.sleep(1)

                except (BadRequest, Forbidden) as e:
                    print(f"[Bot {self.bot_number}] Error: {e}")
                    await asyncio.sleep(2)
                    msg_index += 1

                except Exception as e:
                    self.stats["errors"] += 1
                    print(f"[Bot {self.bot_number}] NC Error: {e}")
                    await asyncio.sleep(1)
                    msg_index += 1

            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] NC Worker #{worker_id} stopped ({success_count} changes)")
                break
            except Exception as e:
                print(f"[Bot {self.bot_number}] NC Critical Error: {e}")
                await asyncio.sleep(1)

    async def aggressive_nc_loop(self, chat_id: int, target: str, context: ContextTypes.DEFAULT_TYPE, worker_id: int = 1):
        """Aggressive NC with user's custom lines"""
        msg_index = 0
        num_messages = len(NC_LINES)
        success_count = 0
        print(f"[Bot {self.bot_number}] Aggressive NC #{worker_id} STARTED for chat {chat_id}")

        while self.is_running and not GLOBAL_STOP_EVENT.is_set():
            try:
                delay = self.chat_delays.get(chat_id, 0)
                current_msg = NC_LINES[msg_index % num_messages]
                display_name = current_msg.format(target=target)

                try:
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name[:100])
                    msg_index += 1
                    success_count += 1
                    self.stats["sent"] += 1

                    if success_count % 50 == 0:
                        print(f"[Bot {self.bot_number}] Aggressive NC #{worker_id}: {success_count}")

                    if delay > 0:
                        await asyncio.sleep(delay)

                except RetryAfter as e:
                    wait_time = e.retry_after
                    await asyncio.sleep(wait_time + 0.5)

                except (TimedOut, NetworkError):
                    await asyncio.sleep(1)

                except (BadRequest, Forbidden):
                    await asyncio.sleep(2)
                    msg_index += 1

                except Exception:
                    self.stats["errors"] += 1
                    await asyncio.sleep(1)
                    msg_index += 1

            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] Aggressive NC #{worker_id} stopped ({success_count})")
                break
            except Exception:
                await asyncio.sleep(1)

    async def custom_name_change_loop(self, chat_id: int, custom_name: str, context: ContextTypes.DEFAULT_TYPE, worker_id: int = 1, mode: str = "emoji"):
        """Custom name change with emojis/flags/hearts"""
        success_count = 0
        print(f"[Bot {self.bot_number}] Custom NC #{worker_id} ({mode}) STARTED for chat {chat_id}")

        emoji_list = HEART_EMOJIS if mode == "emoji" else FLAGS if mode == "flag" else HEARTS

        while self.is_running and not GLOBAL_STOP_EVENT.is_set():
            try:
                delay = self.chat_delays.get(chat_id, 0)
                emoji = random.choice(emoji_list)
                display_name = f"{emoji} {custom_name} {emoji}"

                try:
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name[:100])
                    success_count += 1
                    self.stats["sent"] += 1

                    if success_count % 50 == 0:
                        print(f"[Bot {self.bot_number}] Custom NC #{worker_id}: {success_count}")

                    if delay > 0:
                        await asyncio.sleep(delay)

                except RetryAfter as e:
                    wait_time = e.retry_after
                    await asyncio.sleep(wait_time + 0.5)

                except (TimedOut, NetworkError):
                    await asyncio.sleep(1)

                except (BadRequest, Forbidden):
                    await asyncio.sleep(2)

                except Exception:
                    self.stats["errors"] += 1
                    await asyncio.sleep(1)

            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] Custom NC #{worker_id} stopped ({success_count})")
                break
            except Exception:
                await asyncio.sleep(1)

    async def slide_loop(self, chat_id: int, target: str, context: ContextTypes.DEFAULT_TYPE, worker_id: int = 1):
        """Slide reply loop with user's slide lines"""
        msg_index = 0
        num_messages = len(SLIDE_LINES)
        success_count = 0
        print(f"[Bot {self.bot_number}] Slide #{worker_id} STARTED for chat {chat_id}")

        while self.is_running and not GLOBAL_STOP_EVENT.is_set():
            try:
                delay = self.chat_delays.get(chat_id, 0)
                current_msg = SLIDE_LINES[msg_index % num_messages]
                message = current_msg.format(target=target)

                try:
                    await context.bot.send_message(chat_id=chat_id, text=message)
                    msg_index += 1
                    success_count += 1
                    self.stats["sent"] += 1

                    if success_count % 50 == 0:
                        print(f"[Bot {self.bot_number}] Slide #{worker_id}: {success_count}")

                    if delay > 0:
                        await asyncio.sleep(delay)

                except RetryAfter as e:
                    wait_time = e.retry_after
                    await asyncio.sleep(wait_time + 0.5)

                except (TimedOut, NetworkError):
                    await asyncio.sleep(1)

                except (BadRequest, Forbidden):
                    await asyncio.sleep(2)
                    msg_index += 1

                except Exception:
                    self.stats["errors"] += 1
                    await asyncio.sleep(1)
                    msg_index += 1

            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] Slide #{worker_id} stopped ({success_count})")
                break
            except Exception:
                await asyncio.sleep(1)

    async def raid_nc_loop(self, chat_id: int, name: str, context: ContextTypes.DEFAULT_TYPE, worker_id: int = 1):
        """Fast raid NC mode"""
        success_count = 0
        styles = ["🔥", "⚡", "💀", "🎯", "🚀", "💣"]
        print(f"[Bot {self.bot_number}] RAID NC #{worker_id} STARTED for chat {chat_id}")

        while self.is_running and not GLOBAL_STOP_EVENT.is_set():
            try:
                delay = self.chat_delays.get(chat_id, 0.2)  # Faster default
                style = styles[success_count % len(styles)]
                display_name = f"{style} {name} | RAID MODE {style}"

                try:
                    await context.bot.set_chat_title(chat_id=chat_id, title=display_name[:100])
                    success_count += 1
                    self.stats["sent"] += 1

                    if success_count % 100 == 0:
                        print(f"[Bot {self.bot_number}] RAID NC #{worker_id}: {success_count}")

                    await asyncio.sleep(delay)

                except RetryAfter as e:
                    wait_time = e.retry_after
                    await asyncio.sleep(wait_time + 0.5)

                except (TimedOut, NetworkError):
                    await asyncio.sleep(0.5)

                except (BadRequest, Forbidden):
                    await asyncio.sleep(1)

                except Exception:
                    self.stats["errors"] += 1
                    await asyncio.sleep(0.5)

            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] RAID NC #{worker_id} stopped ({success_count})")
                break
            except Exception:
                await asyncio.sleep(1)

    async def spam_loop(self, chat_id: int, target_name: str, context: ContextTypes.DEFAULT_TYPE, worker_id: int = 1):
        """Spam loop"""
        success_count = 0
        print(f"[Bot {self.bot_number}] Spam Worker #{worker_id} STARTED for chat {chat_id}")

        while self.is_running and not GLOBAL_STOP_EVENT.is_set():
            try:
                delay = self.chat_delays.get(chat_id, 0)
                spam_msg = random.choice(SPAM_MESSAGES).format(target=target_name)

                try:
                    await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                    success_count += 1
                    self.stats["sent"] += 1

                    if success_count % 100 == 0:
                        print(f"[Bot {self.bot_number}] Spam #{worker_id}: {success_count}")

                    if delay > 0:
                        await asyncio.sleep(delay)

                except RetryAfter as e:
                    wait_time = e.retry_after
                    await asyncio.sleep(wait_time + 0.5)

                except (TimedOut, NetworkError):
                    await asyncio.sleep(1)

                except (BadRequest, Forbidden):
                    await asyncio.sleep(2)

                except Exception:
                    self.stats["errors"] += 1
                    await asyncio.sleep(1)

            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] Spam #{worker_id} stopped ({success_count})")
                break
            except Exception:
                await asyncio.sleep(1)

    async def reply_loop(self, chat_id: int, target_name: str, context: ContextTypes.DEFAULT_TYPE):
        """Reply to messages loop"""
        success_count = 0
        print(f"[Bot {self.bot_number}] Reply LOOP started for chat {chat_id}")

        while self.is_running and not GLOBAL_STOP_EVENT.is_set():
            try:
                delay = self.chat_delays.get(chat_id, 0)

                if chat_id in self.pending_replies and self.pending_replies[chat_id]:
                    async with self.get_lock(chat_id):
                        messages_to_reply = self.pending_replies[chat_id].copy()
                        self.pending_replies[chat_id] = []

                    for msg_id in messages_to_reply:
                        try:
                            reply_msg = random.choice(REPLY_MESSAGES).format(target=target_name)
                            await context.bot.send_message(
                                chat_id=chat_id,
                                text=reply_msg,
                                reply_to_message_id=msg_id
                            )
                            success_count += 1
                            self.stats["sent"] += 1

                            if delay > 0:
                                await asyncio.sleep(delay)

                        except asyncio.CancelledError:
                            raise
                        except RetryAfter as e:
                            await asyncio.sleep(e.retry_after + 0.5)
                        except (TimedOut, NetworkError):
                            pass
                        except (BadRequest, Forbidden):
                            pass
                        except Exception:
                            self.stats["errors"] += 1
                else:
                    await asyncio.sleep(0.1)

            except asyncio.CancelledError:
                print(f"[Bot {self.bot_number}] Reply stopped ({success_count})")
                break
            except Exception:
                await asyncio.sleep(1)

    async def message_collector(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Collect messages for reply feature"""
        if not update.message:
            return
        chat_id = update.effective_chat.id
        if chat_id in self.active_reply_targets:
            msg_id = update.message.message_id
            async with self.get_lock(chat_id):
                if chat_id not in self.pending_replies:
                    self.pending_replies[chat_id] = []
                self.pending_replies[chat_id].append(msg_id)

    # ==================== COMMAND HANDLERS ====================

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        help_text = """
𝐀ɴ𝐎ꜱ!! 𝐍ᴀ𝐌ᴇ 𝐂ʜᴀɴɢE 𝐂ᴏᴍᴍᴀɴᴅ𓍼ֶָ֢⊹ ࣪ ˖
`/nc`	`/nc <name>`	
`/nc2`	`/nc2 <target>`
`/ncemo`	`/ncemo <name>`	
`/ncflag`	`/ncflag <name>`
`/ncheart`	`/ncheart <name>`	
`/raidnc`	`/raidnc <name>`
`/mixnc`	`/mixnc <name>`	
`/stopnc`	`/stopnc`		
❦𝐒ʟɪᴅᴇ 𝐀ɴᴅ 𝐒ᴘᴀᴍ ᴄᴏᴍᴍᴀɴᴅ𓍼ֶָ֢⊹ ࣪ ˖
`/slide2`	`/slide2 <target>`	
`/spam`	`/spam <target>`	
`/stopslide`	`/stopslide`	
`/stopspam`	`/stopspam`		
❦𝐑ᴇᴘʟʏ 𝐂ᴏᴍᴍᴀɴᴅ𓍼ֶָ֢⊹ ࣪ ˖
	`/reply`	`/reply <target>`
`/stopreply`	`/stopreply`	
❦𝐒ᴇᴛᴛɪɴɢ 𝐂ᴏᴍᴍᴀɴᴅ𓍼ֶָ֢⊹ ࣪ ˖
`/threads`	`/threads <1-10>`	
`/delay`	`/delay <seconds>`	
❦𝐒ᴜᴅᴏ 𝐂ᴏᴍᴍᴀɴᴅ𓍼ֶָ֢⊹ ࣪ ˖
`/sudo`	`/sudo <user_id>`		
`/unsudo`	`/unsudo <user_id>`
`/sudolist`	`/sudolist`	
❦𝐒ᴛᴏᴘ 𝐂ᴏᴍᴍᴀɴᴅ𓍼ֶָ֢⊹ ࣪ ˖
`/stopall`	
`/superstop`	
❦𝐈ɴғᴏ 𝐂ᴏᴍᴍᴀɴᴅ𓍼ֶָ֢⊹ ࣪ ˖
Command	Description	
`/start`	Show help menu	
`/help`	Show help menu	
`/status`	Show bot statistics	

⚡ Bot {self.bot_number} | Owner: {OWNER_ID}
"""
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

    async def nc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~nc <name>")
            return

        base_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_name_change_tasks:
                await self.safe_cancel_tasks(self.active_name_change_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.name_change_loop(chat_id, base_name, context, i + 1))
                tasks.append(task)

            self.active_name_change_tasks[chat_id] = tasks

        await update.message.reply_text(f"✅ [Bot {self.bot_number}] NC started with {num_threads} threads!")

    async def nc2_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Aggressive NC with user's custom lines"""
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~nc2 <target>")
            return

        target = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_name_change_tasks:
                await self.safe_cancel_tasks(self.active_name_change_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.aggressive_nc_loop(chat_id, target, context, i + 1))
                tasks.append(task)

            self.active_name_change_tasks[chat_id] = tasks

        await update.message.reply_text(f"✅ [Bot {self.bot_number}] Aggressive NC started with {num_threads} threads!")

    async def ncemo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~ncemo <name>")
            return

        custom_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_custom_nc_tasks:
                await self.safe_cancel_tasks(self.active_custom_nc_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.custom_name_change_loop(chat_id, custom_name, context, i + 1, "emoji"))
                tasks.append(task)

            self.active_custom_nc_tasks[chat_id] = tasks

        await update.message.reply_text(f"✅ [Bot {self.bot_number}] Emoji NC started!")

    async def ncflag_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~ncflag <name>")
            return

        custom_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_custom_nc_tasks:
                await self.safe_cancel_tasks(self.active_custom_nc_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.custom_name_change_loop(chat_id, custom_name, context, i + 1, "flag"))
                tasks.append(task)

            self.active_custom_nc_tasks[chat_id] = tasks

        await update.message.reply_text(f"✅ [Bot {self.bot_number}] Flag NC started!")

    async def ncheart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~ncheart <name>")
            return

        custom_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_custom_nc_tasks:
                await self.safe_cancel_tasks(self.active_custom_nc_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.custom_name_change_loop(chat_id, custom_name, context, i + 1, "heart"))
                tasks.append(task)

            self.active_custom_nc_tasks[chat_id] = tasks

        await update.message.reply_text(f"✅ [Bot {self.bot_number}] Heart NC started!")

    async def raidnc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Fast raid NC mode"""
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~raidnc <name>")
            return

        name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_name_change_tasks:
                await self.safe_cancel_tasks(self.active_name_change_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 2)  # Default 2 for raid
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.raid_nc_loop(chat_id, name, context, i + 1))
                tasks.append(task)

            self.active_name_change_tasks[chat_id] = tasks

        await update.message.reply_text(f"⚡ [Bot {self.bot_number}] RAID NC started with {num_threads} threads!")

    async def mixnc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mixed style NC"""
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~mixnc <name>")
            return

        name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            # Stop existing
            if chat_id in self.active_name_change_tasks:
                await self.safe_cancel_tasks(self.active_name_change_tasks[chat_id])
            if chat_id in self.active_custom_nc_tasks:
                await self.safe_cancel_tasks(self.active_custom_nc_tasks[chat_id])

            # Start mixed - some threads with standard, some with custom
            num_threads = self.chat_threads.get(chat_id, 2)
            tasks = []

            # Half aggressive, half emoji
            for i in range(num_threads // 2):
                task = asyncio.create_task(self.aggressive_nc_loop(chat_id, name, context, i + 1))
                tasks.append(task)

            for i in range(num_threads // 2, num_threads):
                task = asyncio.create_task(self.custom_name_change_loop(chat_id, name, context, i + 1, "emoji"))
                tasks.append(task)

            self.active_name_change_tasks[chat_id] = tasks

        await update.message.reply_text(f"🎭 [Bot {self.bot_number}] Mixed NC started!")

    async def stop_nc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            stopped = 0
            if chat_id in self.active_name_change_tasks:
                await self.safe_cancel_tasks(self.active_name_change_tasks[chat_id])
                stopped += len(self.active_name_change_tasks[chat_id])
                del self.active_name_change_tasks[chat_id]

            if chat_id in self.active_custom_nc_tasks:
                await self.safe_cancel_tasks(self.active_custom_nc_tasks[chat_id])
                stopped += len(self.active_custom_nc_tasks[chat_id])
                del self.active_custom_nc_tasks[chat_id]

            if stopped > 0:
                await update.message.reply_text(f"🛑 [Bot {self.bot_number}] Stopped {stopped} NC tasks!")
            else:
                await update.message.reply_text(f"ℹ️ [Bot {self.bot_number}] No active NC!")

    async def slide2_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Slide reply with user's custom lines"""
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~slide2 <target>")
            return

        target = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_slide_tasks:
                await self.safe_cancel_tasks(self.active_slide_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.slide_loop(chat_id, target, context, i + 1))
                tasks.append(task)

            self.active_slide_tasks[chat_id] = tasks

        await update.message.reply_text(f"✅ [Bot {self.bot_number}] Slide2 started with {num_threads} threads!")

    async def stop_slide_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_slide_tasks:
                count = len(self.active_slide_tasks[chat_id])
                await self.safe_cancel_tasks(self.active_slide_tasks[chat_id])
                del self.active_slide_tasks[chat_id]
                await update.message.reply_text(f"🛑 [Bot {self.bot_number}] Stopped {count} slide tasks!")
            else:
                await update.message.reply_text(f"ℹ️ [Bot {self.bot_number}] No active slide!")

    async def spam_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~spam <target_name>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_spam_tasks:
                await self.safe_cancel_tasks(self.active_spam_tasks[chat_id])

            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = []
            for i in range(num_threads):
                task = asyncio.create_task(self.spam_loop(chat_id, target_name, context, i + 1))
                tasks.append(task)

            self.active_spam_tasks[chat_id] = tasks

        await update.message.reply_text(f"✅ [Bot {self.bot_number}] Spam started with {num_threads} threads!")

    async def stop_spam_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_spam_tasks:
                count = len(self.active_spam_tasks[chat_id])
                await self.safe_cancel_tasks(self.active_spam_tasks[chat_id])
                del self.active_spam_tasks[chat_id]
                await update.message.reply_text(f"🛑 [Bot {self.bot_number}] Stopped {count} spam tasks!")
            else:
                await update.message.reply_text(f"ℹ️ [Bot {self.bot_number}] No active spam!")

    async def reply_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat = update.effective_chat
        if chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
            await update.message.reply_text("❌ Only works in groups!")
            return

        if not context.args:
            await update.message.reply_text("Usage: ~reply <target_name>")
            return

        target_name = " ".join(context.args)
        chat_id = chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_reply_tasks:
                self.active_reply_tasks[chat_id].cancel()

            self.active_reply_targets[chat_id] = target_name
            self.pending_replies[chat_id] = []
            task = asyncio.create_task(self.reply_loop(chat_id, target_name, context))
            self.active_reply_tasks[chat_id] = task

        await update.message.reply_text(f"✅ [Bot {self.bot_number}] Reply mode started for {target_name}!")

    async def stop_reply_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            if chat_id in self.active_reply_tasks:
                self.active_reply_tasks[chat_id].cancel()
                del self.active_reply_tasks[chat_id]
                if chat_id in self.active_reply_targets:
                    del self.active_reply_targets[chat_id]
                if chat_id in self.pending_replies:
                    del self.pending_replies[chat_id]
                await update.message.reply_text(f"🛑 [Bot {self.bot_number}] Reply stopped!")
            else:
                await update.message.reply_text(f"ℹ️ [Bot {self.bot_number}] No active reply!")

    async def set_delay_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: ~delay <seconds>")
            return

        try:
            delay = float(context.args[0])
            chat_id = update.effective_chat.id
            self.chat_delays[chat_id] = delay
            await update.message.reply_text(f"✅ [Bot {self.bot_number}] Delay set to {delay}s!")
        except ValueError:
            await update.message.reply_text("❌ Invalid delay value!")

    async def set_threads_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: ~threads <1-10>")
            return

        try:
            threads = int(context.args[0])
            if threads < 1 or threads > 10:
                await update.message.reply_text("❌ Threads must be 1-10!")
                return
            chat_id = update.effective_chat.id
            self.chat_threads[chat_id] = threads
            await update.message.reply_text(f"✅ [Bot {self.bot_number}] Threads set to {threads}!")
        except ValueError:
            await update.message.reply_text("❌ Invalid thread count!")

    async def add_sudo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_main_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: ~sudo <user_id>")
            return

        try:
            user_id = int(context.args[0])
            SUDO_USERS.add(user_id)
            await update.message.reply_text(f"✅ Added {user_id} to sudo users!")
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID!")

    async def remove_sudo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_main_owner(update):
            return

        if not context.args:
            await update.message.reply_text("Usage: ~unsudo <user_id>")
            return

        try:
            user_id = int(context.args[0])
            if user_id in SUDO_USERS:
                SUDO_USERS.discard(user_id)
                await update.message.reply_text(f"✅ Removed {user_id} from sudo!")
            else:
                await update.message.reply_text(f"ℹ️ {user_id} not in sudo!")
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID!")

    async def list_sudo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        if not SUDO_USERS:
            await update.message.reply_text("📋 No sudo users!")
            return

        msg = "📋 <b>Sudo Users:</b>\n\n"
        for uid in SUDO_USERS:
            msg += f"• <code>{uid}</code>\n"
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

    async def stop_all_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        count = await self.stop_all_tasks_globally()
        await update.message.reply_text(f"🛑 [Bot {self.bot_number}] Stopped {count} tasks!")

    async def super_stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        GLOBAL_STOP_EVENT.set()
        total = 0
        for bot in ALL_BOT_INSTANCES.values():
            count = await bot.stop_all_tasks_globally()
            total += count

        await update.message.reply_text(f"🛑 SUPER STOP! Stopped {total} tasks across all bots!")
        await asyncio.sleep(2)
        GLOBAL_STOP_EVENT.clear()

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.check_owner(update):
            return

        uptime = time.time() - self.stats["start_time"]
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)

        status_text = f"""
📊 <b>Bot {self.bot_number} Status</b>

⏱ Uptime: {hours}h {minutes}m {seconds}s
✅ Sent: {self.stats['sent']}
❌ Errors: {self.stats['errors']}
🧵 Spam Tasks: {len(self.active_spam_tasks)}
📝 NC Tasks: {len(self.active_name_change_tasks)}
💬 Reply Tasks: {len(self.active_reply_tasks)}
👥 Sudo Users: {len(SUDO_USERS)}
"""
        await update.message.reply_text(status_text, parse_mode=ParseMode.HTML)


def build_application(token: str, bot_number: int) -> Application:
    bot_instance = BotInstance(bot_number, OWNER_ID)

    app = Application.builder().token(token).build()

    # Command handlers
    app.add_handler(CommandHandler("start", bot_instance.start))
    app.add_handler(CommandHandler("help", bot_instance.start))

    # NC commands
    app.add_handler(CommandHandler("nc", bot_instance.nc_command))
    app.add_handler(CommandHandler("nc2", bot_instance.nc2_command))
    app.add_handler(CommandHandler("ncemo", bot_instance.ncemo_command))
    app.add_handler(CommandHandler("ncflag", bot_instance.ncflag_command))
    app.add_handler(CommandHandler("ncheart", bot_instance.ncheart_command))
    app.add_handler(CommandHandler("raidnc", bot_instance.raidnc_command))
    app.add_handler(CommandHandler("mixnc", bot_instance.mixnc_command))
    app.add_handler(CommandHandler("stopnc", bot_instance.stop_nc_command))

    # Slide commands
    app.add_handler(CommandHandler("slide2", bot_instance.slide2_command))
    app.add_handler(CommandHandler("stopslide", bot_instance.stop_slide_command))

    # Spam commands
    app.add_handler(CommandHandler("spam", bot_instance.spam_command))
    app.add_handler(CommandHandler("stopspam", bot_instance.stop_spam_command))

    # Reply commands
    app.add_handler(CommandHandler("reply", bot_instance.reply_command))
    app.add_handler(CommandHandler("stopreply", bot_instance.stop_reply_command))

    # Settings
    app.add_handler(CommandHandler("delay", bot_instance.set_delay_command))
    app.add_handler(CommandHandler("threads", bot_instance.set_threads_command))

    # Sudo
    app.add_handler(CommandHandler("sudo", bot_instance.add_sudo_command))
    app.add_handler(CommandHandler("unsudo", bot_instance.remove_sudo_command))
    app.add_handler(CommandHandler("sudolist", bot_instance.list_sudo_command))

    # Stop
    app.add_handler(CommandHandler("stopall", bot_instance.stop_all_command))
    app.add_handler(CommandHandler("superstop", bot_instance.super_stop_command))

    # Status
    app.add_handler(CommandHandler("status", bot_instance.status_command))

    # Message collector for reply
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, bot_instance.message_collector))

    return app


async def run_bot(token: str, bot_number: int):
    try:
        app = build_application(token, bot_number)
        print(f"[Bot {bot_number}] Starting...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True, timeout=30)
        print(f"[Bot {bot_number}] Running!")

        while not GLOBAL_STOP_EVENT.is_set():
            await asyncio.sleep(1)

        print(f"[Bot {bot_number}] Stopping...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
    except Exception as e:
        print(f"[Bot {bot_number}] Error: {e}")
        traceback.print_exc()


async def main():
    print("=" * 70)
    print("⚡⚡⚡ ANOS!! MULTI BOT - COMPLETE VERSION ⚡⚡⚡")
    print("=" * 70)

    def signal_handler(sig, frame):
        print("\n🛑 Shutdown signal received...")
        GLOBAL_STOP_EVENT.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    tasks = []
    for i, token in enumerate(BOT_TOKENS, 1):
        task = asyncio.create_task(run_bot(token, i))
        tasks.append(task)
        await asyncio.sleep(0.3)

    print(f"\n✅ Started {len(BOT_TOKENS)} bots!")
    print("Press Ctrl+C to stop all bots.\n")

    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        print(f"Main error: {e}")
    finally:
        GLOBAL_STOP_EVENT.set()
        for bot in ALL_BOT_INSTANCES.values():
            await bot.stop_all_tasks_globally()
        print("\n👋 All bots stopped!")


if __name__ == "__main__":
    asyncio.run(main())
