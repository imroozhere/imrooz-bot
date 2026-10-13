import os
import random
import requests
import telebot
from telebot import types

# Telegram API fix & Token
TELEGRAM_API_URL = 'https://api.telegram.org/bot{0}/{1}'
BOT_TOKEN = '8961049217:AAFWq408kt2YdNPORU-tXfc7X5L2c7PzKFg'
ADMIN_ID = 7055191372

# Binance Pay & BunnyTools details
BINANCE_PAY_ID = '1280231304'
BUNNY_API_KEY = 'bn_f14fb6d6ca7929fc3a637bcedd3c4c0'
BUNNY_ORDER_URL = 'https://bunnytoolbot.tech/api/v1/order/create'
BUNNY_PRODUCTS_URL = 'https://bunnytoolbot.tech/api/v1/products'

bot = telebot.TeleBot(BOT_TOKEN)

user_ids = set()
user_balances = {}
deposit_awaiting_amt = set()
active_deposits = {}
user_languages = {}

# Images Dictionary
IMAGES = {
    'shop': 'shopping_24908_54437.jpg',
    'profile': 'pngtree-casual-man-flat-design-avatar-profile-picture-vector-png-image_1556598.png',
    'history': '18348018.png',
    'wallet': 'wallet-money-cartoon-vector-icon-illustration-finance-business-icon-isolated-flat-vector_128676-12862.png',
    'support': 'man-is-wearing-headphones-headset-minimal-logo-depicting-it-support-services-minimalist-simple-modern-vector-logo-design_558213-64874.jpg',
    'api': 'chain-icon-1076610-26264.jpg',
    'lang': 'language.jpg',
}

# Products Catalog with Stock Status Connected
PRODUCTS = {
    'buy_zoom': {
        'id': 101,
        'match_name': 'Zoom Pro 28 Days',
        'name': 'ZOOM PRO (28 DAYS)',
        'selling_price': 4.0,
        'base_label': '💻 ZOOM PRO 28D – 4.0 USDT (OUT OF STOCK)',
    },
    'buy_canva': {
        'id': 102,
        'match_name': 'Canva Pro Edu 1 Year Invite',
        'name': 'CANVA PRO EDU (1 YEAR INVITE)',
        'selling_price': 1.5,
        'base_label': '🎨 CANVA PRO EDU 1Y – 1.5 USDT (OUT OF STOCK)',
    },
    'buy_duolingo': {
        'id': 103,
        'match_name': 'Super Duolingo 1 Year Promo Code',
        'name': 'SUPER DUOLINGO (1 YEAR PROMO CODE)',
        'selling_price': 3.0,
        'base_label': '🦉 SUPER DUOLINGO 1Y – 3.0 USDT (OUT OF STOCK)',
    },
    'buy_spotify': {
        'id': 104,
        'match_name': 'Spotify Premium 3 Month Redeem Link',
        'name': 'SPOTIFY PREMIUM (3 MONTH REDEEM LINK)',
        'selling_price': 2.0,
        'base_label': '🎧 SPOTIFY 3M LINK – 2.0 USDT (OUT OF STOCK)',
    },
    'buy_surfshark': {
        'id': 105,
        'match_name': 'Surfshark VPN 2 Month Coupon',
        'name': 'SURFSHARK VPN (2 MONTH COUPON)',
        'selling_price': 3.0,
        'base_label': '🦈 SURFSHARK VPN 2M – 3.0 USDT (OUT OF STOCK)',
    },
    'buy_nord': {
        'id': 106,
        'match_name': 'NordVPN 3M Account',
        'name': 'NORDVPN (3M ACCOUNT)',
        'selling_price': 4.5,
        'base_label': '🛡️ NORDVPN 3M ACC – 4.5 USDT (OUT OF STOCK)',
    },
    'buy_amazon': {
        'id': 107,
        'match_name': 'Amazon Prime Video 1 Month',
        'name': 'AMAZON PRIME VIDEO (1 MONTH)',
        'selling_price': 2.0,
        'base_label': '📦 AMAZON PRIME 1M – 2.0 USDT (OUT OF STOCK)',
    },
    'buy_capcut': {
        'id': 108,
        'match_name': 'CapCut Pro 1 Month',
        'name': 'CAPCUT PRO (1 MONTH)',
        'selling_price': 2.7,
        'base_label': '🎬 CAPCUT PRO 1M – 2.7 USDT (IN STOCK 24)',
    },
    'buy_gemini': {
        'id': 109,
        'match_name': 'Gemini Pro 18 Months',
        'name': 'GEMINI PRO (18 MONTHS)',
        'selling_price': 1.5,
        'base_label': '✨ GEMINI PRO 18M – 1.5 USDT (IN STOCK 407)',
    },
    'buy_capcut7d': {
        'id': 110,
        'match_name': 'CapCut Pro 7 Days',
        'name': 'CAPCUT PRO (7 DAYS)',
        'selling_price': 0.9,
        'base_label': '🎬 CAPCUT PRO 7D – 0.9 USDT (OUT OF STOCK)',
    },
    'buy_muse': {
        'id': 111,
        'match_name': 'Muse AI 2B Tokens',
        'name': 'MUSE AI (2B TOKENS)',
        'selling_price': 3.3,
        'base_label': '🔮 MUSE AI 2B TOKENS – 3.3 USDT (OUT OF STOCK)',
    },
    'buy_crunchyroll': {
        'id': 112,
        'match_name': 'Crunchyroll 1M Link',
        'name': 'CRUNCHYROLL (1M LINK)',
        'selling_price': 2.0,
        'base_label': '🍙 CRUNCHYROLL 1M LINK – 2.0 USDT (IN STOCK)',
    },
}


# Main Menu Markup with all options (Shop, Wallet, Profile, Support, etc.)
def get_main_menu():
  markup = types.InlineKeyboardMarkup(row_width=2)
  markup.add(
      types.InlineKeyboardButton('🛍️ Shop Catalog', callback_data='menu_shop'),
      types.InlineKeyboardButton('💰 Wallet / Deposit', callback_data='menu_wallet'),
  )
  markup.add(
      types.InlineKeyboardButton('👤 Profile', callback_data='menu_profile'),
      types.InlineKeyboardButton('📜 Purchase History', callback_data='menu_history'),
  )
  markup.add(
      types.InlineKeyboardButton('🎧 Support', callback_data='menu_support'),
      types.InlineKeyboardButton('🌐 Language', callback_data='menu_lang'),
  )
  return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_ids.add(message.chat.id)
  bot.send_message(
      message.chat.id,
      '🌟 **WELCOME TO IMROOZ AI STORE** 🌟\n\nChoose an option from the menu below:',
      reply_markup=get_main_menu(),
      parse_mode='Markdown',
  )


# Callback Query Handler for Menu Navigation & Products
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  chat_id = call.message.chat.id
  
  if call.data == 'menu_shop':
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, prod in PRODUCTS.items():
      markup.add(types.InlineKeyboardButton(prod['base_label'], callback_data=key))
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        '🛒 **IMROOZ AI STORE – AVAILABLE STOCK**\n\nSELECT A PRODUCT TO BUY INSTANTLY:',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_wallet':
    balance = user_balances.get(chat_id, 0.0)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('💳 Deposit via Binance Pay', callback_data='deposit_binance'))
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        f'💰 **YOUR WALLET**\n\nCurrent Balance: **{balance} USDT**',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_profile':
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        f'👤 **USER PROFILE**\n\nTelegram ID: `{chat_id}`\nBalance: {user_balances.get(chat_id, 0.0)} USDT',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_history':
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        '📜 **PURCHASE HISTORY**\n\nYou have no past purchases yet.',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_support':
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        '🎧 **CUSTOMER SUPPORT**\n\nFor any issues, contact admin directly.',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_lang':
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        '🌐 **LANGUAGE SELECTION**\n\nCurrent Language: English',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'main_menu':
    bot.edit_message_text(
        '🌟 **WELCOME TO IMROOZ AI STORE** 🌟\n\nChoose an option from the menu below:',
        chat_id,
        call.message.message_id,
        reply_markup=get_main_menu(),
        parse_mode='Markdown',
    )

  elif call.data == 'deposit_binance':
    bot.answer_callback_query(call.id, 'Binance Pay deposit system active!')


@bot.message_handler(commands=['addstock'])
def add_new_stock(message):
  if message.from_user.id == ADMIN_ID:
    text = message.text.replace('/addstock', '').strip()
    if text:
      for uid in user_ids:
        try:
          bot.send_message(uid, f'🚨 **Stock Added Now!** 🚨\n\n{text}', parse_mode='Markdown')
        except Exception as e:
          pass
      bot.reply_to(message, '✅ Stock update ho gaya hai aur sabhi users ko broadcast kar diya gaya hai!')
    else:
      bot.reply_to(message, '⚠️ Barah-e-karam details likhein. Misal: /addstock CapCut Pro 1M - In Stock 50')
  else:
    bot.reply_to(message, '❌ Aap yeh command use nahi kar sakte!')


@bot.message_handler(commands=['stock'])
def check_stock(message):
  catalog_text = '🛍️ **IMROOZ VIP STORE – AVAILABLE STOCK**\n\n'
  for prod, details in PRODUCTS.items():
    catalog_text += f"• {details['base_label']}\n"
  bot.reply_to(message, catalog_text, parse_mode='Markdown')


print('Bot successfully chal raha hai...')
bot.infinity_polling()
import os
import random
import requests
import telebot
from telebot import types

# Telegram API fix & Token
TELEGRAM_API_URL = 'https://api.telegram.org/bot{0}/{1}'
BOT_TOKEN = '8961049217:AAFWq408kt2YdNPORU-tXfc7X5L2c7PzKFg'
ADMIN_ID = 7055191372

# Binance Pay & BunnyTools details
BINANCE_PAY_ID = '1280231304'
BUNNY_API_KEY = 'bn_f14fb6d6ca7929fc3a637bcedd3c4c0'
BUNNY_ORDER_URL = 'https://bunnytoolbot.tech/api/v1/order/create'
BUNNY_PRODUCTS_URL = 'https://bunnytoolbot.tech/api/v1/products'

bot = telebot.TeleBot(BOT_TOKEN)

user_ids = set()
user_balances = {}
deposit_awaiting_amt = set()
active_deposits = {}
user_languages = {}

# Images Dictionary
IMAGES = {
    'shop': 'shopping_24908_54437.jpg',
    'profile': 'pngtree-casual-man-flat-design-avatar-profile-picture-vector-png-image_1556598.png',
    'history': '18348018.png',
    'wallet': 'wallet-money-cartoon-vector-icon-illustration-finance-business-icon-isolated-flat-vector_128676-12862.png',
    'support': 'man-is-wearing-headphones-headset-minimal-logo-depicting-it-support-services-minimalist-simple-modern-vector-logo-design_558213-64874.jpg',
    'api': 'chain-icon-1076610-26264.jpg',
    'lang': 'language.jpg',
}

# Products Catalog with Stock Status Connected
PRODUCTS = {
    'buy_zoom': {
        'id': 101,
        'match_name': 'Zoom Pro 28 Days',
        'name': 'ZOOM PRO (28 DAYS)',
        'selling_price': 4.0,
        'base_label': '💻 ZOOM PRO 28D – 4.0 USDT (OUT OF STOCK)',
    },
    'buy_canva': {
        'id': 102,
        'match_name': 'Canva Pro Edu 1 Year Invite',
        'name': 'CANVA PRO EDU (1 YEAR INVITE)',
        'selling_price': 1.5,
        'base_label': '🎨 CANVA PRO EDU 1Y – 1.5 USDT (OUT OF STOCK)',
    },
    'buy_duolingo': {
        'id': 103,
        'match_name': 'Super Duolingo 1 Year Promo Code',
        'name': 'SUPER DUOLINGO (1 YEAR PROMO CODE)',
        'selling_price': 3.0,
        'base_label': '🦉 SUPER DUOLINGO 1Y – 3.0 USDT (OUT OF STOCK)',
    },
    'buy_spotify': {
        'id': 104,
        'match_name': 'Spotify Premium 3 Month Redeem Link',
        'name': 'SPOTIFY PREMIUM (3 MONTH REDEEM LINK)',
        'selling_price': 2.0,
        'base_label': '🎧 SPOTIFY 3M LINK – 2.0 USDT (OUT OF STOCK)',
    },
    'buy_surfshark': {
        'id': 105,
        'match_name': 'Surfshark VPN 2 Month Coupon',
        'name': 'SURFSHARK VPN (2 MONTH COUPON)',
        'selling_price': 3.0,
        'base_label': '🦈 SURFSHARK VPN 2M – 3.0 USDT (OUT OF STOCK)',
    },
    'buy_nord': {
        'id': 106,
        'match_name': 'NordVPN 3M Account',
        'name': 'NORDVPN (3M ACCOUNT)',
        'selling_price': 4.5,
        'base_label': '🛡️ NORDVPN 3M ACC – 4.5 USDT (OUT OF STOCK)',
    },
    'buy_amazon': {
        'id': 107,
        'match_name': 'Amazon Prime Video 1 Month',
        'name': 'AMAZON PRIME VIDEO (1 MONTH)',
        'selling_price': 2.0,
        'base_label': '📦 AMAZON PRIME 1M – 2.0 USDT (OUT OF STOCK)',
    },
    'buy_capcut': {
        'id': 108,
        'match_name': 'CapCut Pro 1 Month',
        'name': 'CAPCUT PRO (1 MONTH)',
        'selling_price': 2.7,
        'base_label': '🎬 CAPCUT PRO 1M – 2.7 USDT (IN STOCK 24)',
    },
    'buy_gemini': {
        'id': 109,
        'match_name': 'Gemini Pro 18 Months',
        'name': 'GEMINI PRO (18 MONTHS)',
        'selling_price': 1.5,
        'base_label': '✨ GEMINI PRO 18M – 1.5 USDT (IN STOCK 407)',
    },
    'buy_capcut7d': {
        'id': 110,
        'match_name': 'CapCut Pro 7 Days',
        'name': 'CAPCUT PRO (7 DAYS)',
        'selling_price': 0.9,
        'base_label': '🎬 CAPCUT PRO 7D – 0.9 USDT (OUT OF STOCK)',
    },
    'buy_muse': {
        'id': 111,
        'match_name': 'Muse AI 2B Tokens',
        'name': 'MUSE AI (2B TOKENS)',
        'selling_price': 3.3,
        'base_label': '🔮 MUSE AI 2B TOKENS – 3.3 USDT (OUT OF STOCK)',
    },
    'buy_crunchyroll': {
        'id': 112,
        'match_name': 'Crunchyroll 1M Link',
        'name': 'CRUNCHYROLL (1M LINK)',
        'selling_price': 2.0,
        'base_label': '🍙 CRUNCHYROLL 1M LINK – 2.0 USDT (IN STOCK)',
    },
}


# Main Menu Markup with all options (Shop, Wallet, Profile, Support, etc.)
def get_main_menu():
  markup = types.InlineKeyboardMarkup(row_width=2)
  markup.add(
      types.InlineKeyboardButton('🛍️ Shop Catalog', callback_data='menu_shop'),
      types.InlineKeyboardButton('💰 Wallet / Deposit', callback_data='menu_wallet'),
  )
  markup.add(
      types.InlineKeyboardButton('👤 Profile', callback_data='menu_profile'),
      types.InlineKeyboardButton('📜 Purchase History', callback_data='menu_history'),
  )
  markup.add(
      types.InlineKeyboardButton('🎧 Support', callback_data='menu_support'),
      types.InlineKeyboardButton('🌐 Language', callback_data='menu_lang'),
  )
  return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_ids.add(message.chat.id)
  bot.send_message(
      message.chat.id,
      '🌟 **WELCOME TO IMROOZ AI STORE** 🌟\n\nChoose an option from the menu below:',
      reply_markup=get_main_menu(),
      parse_mode='Markdown',
  )


# Callback Query Handler for Menu Navigation & Products
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  chat_id = call.message.chat.id
  
  if call.data == 'menu_shop':
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, prod in PRODUCTS.items():
      markup.add(types.InlineKeyboardButton(prod['base_label'], callback_data=key))
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        '🛒 **IMROOZ AI STORE – AVAILABLE STOCK**\n\nSELECT A PRODUCT TO BUY INSTANTLY:',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_wallet':
    balance = user_balances.get(chat_id, 0.0)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('💳 Deposit via Binance Pay', callback_data='deposit_binance'))
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        f'💰 **YOUR WALLET**\n\nCurrent Balance: **{balance} USDT**',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_profile':
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        f'👤 **USER PROFILE**\n\nTelegram ID: `{chat_id}`\nBalance: {user_balances.get(chat_id, 0.0)} USDT',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_history':
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        '📜 **PURCHASE HISTORY**\n\nYou have no past purchases yet.',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_support':
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        '🎧 **CUSTOMER SUPPORT**\n\nFor any issues, contact admin directly.',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'menu_lang':
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔙 Back to Main Menu', callback_data='main_menu'))
    bot.edit_message_text(
        '🌐 **LANGUAGE SELECTION**\n\nCurrent Language: English',
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='Markdown',
    )

  elif call.data == 'main_menu':
    bot.edit_message_text(
        '🌟 **WELCOME TO IMROOZ AI STORE** 🌟\n\nChoose an option from the menu below:',
        chat_id,
        call.message.message_id,
        reply_markup=get_main_menu(),
        parse_mode='Markdown',
    )

  elif call.data == 'deposit_binance':
    bot.answer_callback_query(call.id, 'Binance Pay deposit system active!')


@bot.message_handler(commands=['addstock'])
def add_new_stock(message):
  if message.from_user.id == ADMIN_ID:
    text = message.text.replace('/addstock', '').strip()
    if text:
      for uid in user_ids:
        try:
          bot.send_message(uid, f'🚨 **Stock Added Now!** 🚨\n\n{text}', parse_mode='Markdown')
        except Exception as e:
          pass
      bot.reply_to(message, '✅ Stock update ho gaya hai aur sabhi users ko broadcast kar diya gaya hai!')
    else:
      bot.reply_to(message, '⚠️ Barah-e-karam details likhein. Misal: /addstock CapCut Pro 1M - In Stock 50')
  else:
    bot.reply_to(message, '❌ Aap yeh command use nahi kar sakte!')


@bot.message_handler(commands=['stock'])
def check_stock(message):
  catalog_text = '🛍️ **IMROOZ VIP STORE – AVAILABLE STOCK**\n\n'
  for prod, details in PRODUCTS.items():
    catalog_text += f"• {details['base_label']}\n"
  bot.reply_to(message, catalog_text, parse_mode='Markdown')


print('Bot successfully chal raha hai...')
bot.infinity_polling()
    import os
import random
import requests
import telebot
from telebot import types

# Telegram API fix & Token
TELEGRAM_API_URL = 'https://api.telegram.org/bot{0}/{1}'
BOT_TOKEN = '8961049217:AAFWq408kt2YdNPORU-tXfc7X5L2c7PzKFg'
ADMIN_ID = 7055191372

# Binance Pay & BunnyTools details
BINANCE_PAY_ID = '1280231304'
BUNNY_API_KEY = 'bn_f14fb6d6ca7929fc3a637bcedd3c4c0'
BUNNY_ORDER_URL = 'https://bunnytoolbot.tech/api/v1/order/create'
BUNNY_PRODUCTS_URL = 'https://bunnytoolbot.tech/api/v1/products'

bot = telebot.TeleBot(BOT_TOKEN)

user_ids = set()
user_balances = {}
deposit_awaiting_amt = set()
active_deposits = {}
user_languages = {}

# Images Dictionary
IMAGES = {
    'shop': 'shopping_24908_54437.jpg',
    'profile': 'pngtree-casual-man-flat-design-avatar-profile-picture-vector-png-image_1556598.png',
    'history': '18348018.png',
    'wallet': 'wallet-money-cartoon-vector-icon-illustration-finance-business-icon-isolated-flat-vector_128676-12862.png',
    'support': 'man-is-wearing-headphones-headset-minimal-logo-depicting-it-support-services-minimalist-simple-modern-vector-logo-design_558213-64874.jpg',
    'api': 'chain-icon-1076610-26264.jpg',
    'lang': 'language.jpg',
}

# Products Catalog with Stock Status Connected
PRODUCTS = {
    'buy_zoom': {
        'id': 101,
        'match_name': 'Zoom Pro 28 Days',
        'name': 'ZOOM PRO (28 DAYS)',
        'selling_price': 4.0,
        'base_label': '💻 ZOOM PRO 28D – 4.0 USDT (OUT OF STOCK)',
    },
    'buy_canva': {
        'id': 102,
        'match_name': 'Canva Pro Edu 1 Year Invite',
        'name': 'CANVA PRO EDU (1 YEAR INVITE)',
        'selling_price': 1.5,
        'base_label': '🎨 CANVA PRO EDU 1Y – 1.5 USDT (OUT OF STOCK)',
    },
    'buy_duolingo': {
        'id': 103,
        'match_name': 'Super Duolingo 1 Year Promo Code',
        'name': 'SUPER DUOLINGO (1 YEAR PROMO CODE)',
        'selling_price': 3.0,
        'base_label': '🦉 SUPER DUOLINGO 1Y – 3.0 USDT (OUT OF STOCK)',
    },
    'buy_spotify': {
        'id': 104,
        'match_name': 'Spotify Premium 3 Month Redeem Link',
        'name': 'SPOTIFY PREMIUM (3 MONTH REDEEM LINK)',
        'selling_price': 2.0,
        'base_label': '🎧 SPOTIFY 3M LINK – 2.0 USDT (OUT OF STOCK)',
    },
    'buy_surfshark': {
        'id': 105,
        'match_name': 'Surfshark VPN 2 Month Coupon',
        'name': 'SURFSHARK VPN (2 MONTH COUPON)',
        'selling_price': 3.0,
        'base_label': '🦈 SURFSHARK VPN 2M – 3.0 USDT (OUT OF STOCK)',
    },
    'buy_nord': {
        'id': 106,
        'match_name': 'NordVPN 3M Account',
        'name': 'NORDVPN (3M ACCOUNT)',
        'selling_price': 4.5,
        'base_label': '🛡️ NORDVPN 3M ACC – 4.5 USDT (OUT OF STOCK)',
    },
    'buy_amazon': {
        'id': 107,
        'match_name': 'Amazon Prime Video 1 Month',
        'name': 'AMAZON PRIME VIDEO (1 MONTH)',
        'selling_price': 2.0,
        'base_label': '📦 AMAZON PRIME 1M – 2.0 USDT (OUT OF STOCK)',
    },
    'buy_capcut': {
        'id': 108,
        'match_name': 'CapCut Pro 1 Month',
        'name': 'CAPCUT PRO (1 MONTH)',
        'selling_price': 2.7,
        'base_label': '🎬 CAPCUT PRO 1M – 2.7 USDT (IN STOCK 24)',
    },
    'buy_gemini': {
        'id': 109,
        'match_name': 'Gemini Pro 18 Months',
        'name': 'GEMINI PRO (18 MONTHS)',
        'selling_price': 1.5,
        'base_label': '✨ GEMINI PRO 18M – 1.5 USDT (IN STOCK 407)',
    },
    'buy_capcut7d': {
        'id': 110,
        'match_name': 'CapCut Pro 7 Days',
        'name': 'CAPCUT PRO (7 DAYS)',
        'selling_price': 0.9,
        'base_label': '🎬 CAPCUT PRO 7D – 0.9 USDT (OUT OF STOCK)',
    },
    'buy_muse': {
        'id': 111,
        'match_name': 'Muse AI 2B Tokens',
        'name': 'MUSE AI (2B TOKENS)',
        'selling_price': 3.3,
        'base_label': '🔮 MUSE AI 2B TOKENS – 3.3 USDT (OUT OF STOCK)',
    },
    'buy_crunchyroll': {
        'id': 112,
        'match_name': 'Crunchyroll 1M Link',
        'name': 'CRUNCHYROLL (1M LINK)',
        'selling_price': 2.0,
        'base_label': '🍙 CRUNCHYROLL 1M LINK – 2.0 USDT (IN STOCK)',
    },
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_ids.add(message.chat.id)
  markup = types.InlineKeyboardMarkup(row_width=2)
  for key, prod in PRODUCTS.items():
    markup.add(types.InlineKeyboardButton(prod['base_label'], callback_data=key))
  bot.send_message(
      message.chat.id,
      '🛒 **IMROOZ AI STORE – AVAILABLE STOCK**\n\nSELECT A PRODUCT TO BUY'
      ' INSTANTLY USING YOUR BALANCE:',
      reply_markup=markup,
      parse_mode='Markdown',
  )


@bot.message_handler(commands=['addstock'])
def add_new_stock(message):
  if message.from_user.id == ADMIN_ID:
    text = message.text.replace('/addstock', '').strip()
    if text:
      for uid in user_ids:
        try:
          bot.send_message(
              uid,
              f'🚨 **Stock Added Now!** 🚨\n\n{text}',
              parse_mode='Markdown',
          )
        except Exception as e:
          pass
      bot.reply_to(
          message,
          '✅ Stock update ho gaya hai aur sabhi users ko broadcast kar diya'
          ' gaya hai!',
      )
    else:
      bot.reply_to(
          message,
          '⚠️ Barah-e-karam details likhein. Misal: /addstock CapCut Pro 1M - In'
          ' Stock 50',
      )
  else:
    bot.reply_to(message, '❌ Aap yeh command use nahi kar sakte!')


@bot.message_handler(commands=['stock'])
def check_stock(message):
  catalog_text = '🛍️ **IMROOZ VIP STORE – AVAILABLE STOCK**\n\n'
  for prod, details in PRODUCTS.items():
    catalog_text += f"• {details['match_name']} – {details['base_label']}\n"
  bot.reply_to(message, catalog_text, parse_mode='Markdown')


print('Bot successfully chal raha hai...')
bot.infinity_polling()
import os
import random
import requests
import telebot
from telebot import types

# Telegram API fix & Token
TELEGRAM_API_URL = 'https://api.telegram.org/bot{0}/{1}'
BOT_TOKEN = '8961049217:AAFWq408kt2YdNPORU-tXfc7X5L2c7PzKFg'
ADMIN_ID = 7055191372

# Binance Pay & BunnyTools details
BINANCE_PAY_ID = '1280231304'
BUNNY_API_KEY = 'bn_f14fb6d6ca7929fc3a637bcedd3c4c0'
BUNNY_ORDER_URL = 'https://bunnytoolbot.tech/api/v1/order/create'
BUNNY_PRODUCTS_URL = 'https://bunnytoolbot.tech/api/v1/products'

bot = telebot.TeleBot(BOT_TOKEN)

user_ids = set()
user_balances = {}
deposit_awaiting_amt = set()
active_deposits = {}
user_languages = {}

# Images Dictionary
IMAGES = {
    'shop': 'shopping_24908_54437.jpg',
    'profile': 'pngtree-casual-man-flat-design-avatar-profile-picture-vector-png-image_1556598.png',
    'history': '18348018.png',
    'wallet': 'wallet-money-cartoon-vector-icon-illustration-finance-business-icon-isolated-flat-vector_128676-12862.png',
    'support': 'man-is-wearing-headphones-headset-minimal-logo-depicting-it-support-services-minimalist-simple-modern-vector-logo-design_558213-64874.jpg',
    'api': 'chain-icon-1076610-26264.jpg',
    'lang': 'language.jpg',
}

# Products Catalog with Stock Status Connected
PRODUCTS = {
    'buy_zoom': {
        'id': 101,
        'match_name': 'Zoom Pro 28 Days',
        'name': 'ZOOM PRO (28 DAYS)',
        'selling_price': 4.0,
        'base_label': '💻 ZOOM PRO 28D – 4.0 USDT (OUT OF STOCK)',
    },
    'buy_canva': {
        'id': 102,
        'match_name': 'Canva Pro Edu 1 Year Invite',
        'name': 'CANVA PRO EDU (1 YEAR INVITE)',
        'selling_price': 1.5,
        'base_label': '🎨 CANVA PRO EDU 1Y – 1.5 USDT (OUT OF STOCK)',
    },
    'buy_duolingo': {
        'id': 103,
        'match_name': 'Super Duolingo 1 Year Promo Code',
        'name': 'SUPER DUOLINGO (1 YEAR PROMO CODE)',
        'selling_price': 3.0,
        'base_label': '🦉 SUPER DUOLINGO 1Y – 3.0 USDT (OUT OF STOCK)',
    },
    'buy_spotify': {
        'id': 104,
        'match_name': 'Spotify Premium 3 Month Redeem Link',
        'name': 'SPOTIFY PREMIUM (3 MONTH REDEEM LINK)',
        'selling_price': 2.0,
        'base_label': '🎧 SPOTIFY 3M LINK – 2.0 USDT (OUT OF STOCK)',
    },
    'buy_surfshark': {
        'id': 105,
        'match_name': 'Surfshark VPN 2 Month Coupon',
        'name': 'SURFSHARK VPN (2 MONTH COUPON)',
        'selling_price': 3.0,
        'base_label': '🦈 SURFSHARK VPN 2M – 3.0 USDT (OUT OF STOCK)',
    },
    'buy_nord': {
        'id': 106,
        'match_name': 'NordVPN 3M Account',
        'name': 'NORDVPN (3M ACCOUNT)',
        'selling_price': 4.5,
        'base_label': '🛡️ NORDVPN 3M ACC – 4.5 USDT (OUT OF STOCK)',
    },
    'buy_amazon': {
        'id': 107,
        'match_name': 'Amazon Prime Video 1 Month',
        'name': 'AMAZON PRIME VIDEO (1 MONTH)',
        'selling_price': 2.0,
        'base_label': '📦 AMAZON PRIME 1M – 2.0 USDT (OUT OF STOCK)',
    },
    'buy_capcut': {
        'id': 108,
        'match_name': 'CapCut Pro 1 Month',
        'name': 'CAPCUT PRO (1 MONTH)',
        'selling_price': 2.7,
        'base_label': '🎬 CAPCUT PRO 1M – 2.7 USDT (IN STOCK 24)',
    },
    'buy_gemini': {
        'id': 109,
        'match_name': 'Gemini Pro 18 Months',
        'name': 'GEMINI PRO (18 MONTHS)',
        'selling_price': 1.5,
        'base_label': '✨ GEMINI PRO 18M – 1.5 USDT (IN STOCK 407)',
    },
    'buy_capcut7d': {
        'id': 110,
        'match_name': 'CapCut Pro 7 Days',
        'name': 'CAPCUT PRO (7 DAYS)',
        'selling_price': 0.9,
        'base_label': '🎬 CAPCUT PRO 7D – 0.9 USDT (OUT OF STOCK)',
    },
    'buy_muse': {
        'id': 111,
        'match_name': 'Muse AI 2B Tokens',
        'name': 'MUSE AI (2B TOKENS)',
        'selling_price': 3.3,
        'base_label': '🔮 MUSE AI 2B TOKENS – 3.3 USDT (OUT OF STOCK)',
    },
    'buy_crunchyroll': {
        'id': 112,
        'match_name': 'Crunchyroll 1M Link',
        'name': 'CRUNCHYROLL (1M LINK)',
        'selling_price': 2.0,
        'base_label': '🍙 CRUNCHYROLL 1M LINK – 2.0 USDT (IN STOCK)',
    },
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_ids.add(message.chat.id)
  markup = types.InlineKeyboardMarkup(row_width=2)
  for key, prod in PRODUCTS.items():
    markup.add(types.InlineKeyboardButton(prod['base_label'], callback_data=key))
  bot.send_message(
      message.chat.id,
      '🛒 **IMROOZ AI STORE – AVAILABLE STOCK**\n\nSELECT A PRODUCT TO BUY'
      ' INSTANTLY USING YOUR BALANCE:',
      reply_markup=markup,
      parse_mode='Markdown',
  )


@bot.message_handler(commands=['addstock'])
def add_new_stock(message):
  if message.from_user.id == ADMIN_ID:
    text = message.text.replace('/addstock', '').strip()
    if text:
      for uid in user_ids:
        try:
          bot.send_message(
              uid,
              f'🚨 **Stock Added Now!** 🚨\n\n{text}',
              parse_mode='Markdown',
          )
        except Exception as e:
          pass
      bot.reply_to(
          message,
          '✅ Stock update ho gaya hai aur sabhi users ko broadcast kar diya'
          ' gaya hai!',
      )
    else:
      bot.reply_to(
          message,
          '⚠️ Barah-e-karam details likhein. Misal: /addstock CapCut Pro 1M - In'
          ' Stock 50',
      )
  else:
    bot.reply_to(message, '❌ Aap yeh command use nahi kar sakte!')


@bot.message_handler(commands=['stock'])
def check_stock(message):
  catalog_text = '🛍️ **IMROOZ VIP STORE – AVAILABLE STOCK**\n\n'
  for prod, details in PRODUCTS.items():
    catalog_text += f"• {details['match_name']} – {details['base_label']}\n"
  bot.reply_to(message, catalog_text, parse_mode='Markdown')


print('Bot successfully chal raha hai...')
bot.infinity_polling()
