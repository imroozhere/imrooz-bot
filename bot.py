import os
import random
import requests
import telebot
from telebot import types

# Telegram API fix
telebot.apihelper.API_URL = "https://api.telegram.org/bot{0}/{1}"

BOT_TOKEN = "8961049217:AAFWq408kt2YdNPORU-tXfc7X5L2c7PzKFg"

# Aapki Confirmed Binance Pay ID
BINANCE_PAY_ID = "1286251304"

# BunnyTools API Details
BUNNY_API_KEY = "bn_f14fb6d68ca792bf0eab637bedd5c4e0"
BUNNY_ORDER_URL = "https://bunnytoolbot.tech/api/v1/order/create"
BUNNY_PRODUCTS_URL = "https://bunnytoolbot.tech/api/v1/products"

bot = telebot.TeleBot(BOT_TOKEN)

user_balances = {}
deposit_awaiting_amt = set()
active_deposits = {}
user_languages = {}

# Images Dictionary
IMAGES = {
    "shop": "shopping_24908-54437.jpg",
    "profile": (
        "pngtree-casual-man-flat-design-avatar-profile-picture-vector-png-image_15526568.png"
    ),
    "history": "18348618.png",
    "wallet": (
        "wallet-money-cartoon-vector-icon-illustration-finance-business-icon-isolated-flat-vector_138676-12882.jpg"
    ),
    "support": (
        "man-is-wearing-headphones-headset-minimal-logo-depicting-it-support-services-minimalist-simple-modern-vector-logo-design_538213-64374.jpg"
    ),
    "api": "chain-icon_1076610-26264.jpg",
    "lang": "language.jpg",
}

# Products Catalog with Exact Bunny AI IDs connected directly
PRODUCTS = {
    "buy_zoom": {
        "id": 32,
        "name": "ZOOM PRO (28 DAYS)",
        "selling_price": 4.00,
        "base_label": "💻 ZOOM PRO 28D — 4.0 USDT",
    },
    "buy_canva": {
        "id": 50,
        "name": "CANVA PRO EDU (1 YEAR INVITE)",
        "selling_price": 1.50,
        "base_label": "🎨 CANVA PRO EDU 1Y — 1.5 USDT",
    },
    "buy_duolingo": {
        "id": 12,
        "name": "SUPER DUOLINGO (1 YEAR PROMO CODE)",
        "selling_price": 3.00,
        "base_label": "🦉 SUPER DUOLINGO 1Y — 3.0 USDT",
    },
    "buy_spotify": {
        "id": 11,
        "name": "SPOTIFY PREMIUM (3 MONTH REDEEM LINK)",
        "selling_price": 2.00,
        "base_label": "🎧 SPOTIFY 3M LINK — 2.0 USDT",
    },
    "buy_surfshark": {
        "id": 14,
        "name": "SURFSHARK VPN (2 MONTH COUPON)",
        "selling_price": 3.00,
        "base_label": "🦈 SURFSHARK VPN 2M — 3.0 USDT",
    },
    "buy_nord": {
        "id": 53,
        "name": "NORDVPN (3M ACCOUNT)",
        "selling_price": 4.50,
        "base_label": "🛡️ NORDVPN 3M ACC — 4.5 USDT",
    },
    "buy_amazon": {
        "id": 52,
        "name": "AMAZON PRIME VIDEO (1 MONTH)",
        "selling_price": 2.00,
        "base_label": "📦 AMAZON PRIME 1M — 2.0 USDT",
    },
    "buy_capcut_1m": {
        "id": 3,
        "name": "CAPCUT PRO (1 MONTH PLAN)",
        "selling_price": 2.70,
        "base_label": "⧉ CAPCUT PRO 1M — 2.7 USDT",
    },
    "buy_gemini_18m": {
        "id": 8,
        "name": "GEMINI PRO (18 MONTHS PLAN)",
        "selling_price": 1.50,
        "base_label": "✨ GEMINI PRO 18M — 1.5 USDT",
    },
    "buy_capcut_7d": {
        "id": 30,
        "name": "CAPCUT PRO (7 DAYS PLAN)",
        "selling_price": 0.90,
        "base_label": "⧉ CAPCUT PRO 7D — 0.9 USDT",
    },
    "buy_muse_ai": {
        "id": 42,
        "name": "MUSE AI (2 BILLION TOKENS)",
        "selling_price": 3.30,
        "base_label": "🔮 MUSE AI 2B TOKENS — 3.3 USDT",
    },
    "buy_crunchyroll": {
        "id": 45,
        "name": "CRUNCHYROLL PREMIUM (1 MONTH LINK)",
        "selling_price": 2.00,
        "base_label": "🍙 CRUNCHYROLL 1M LINK — 2.0 USDT",
    },
}


# Ab stock ID ke zariye direct fetch hoga jo kabhi fail nahi hoga
def get_live_stock_map():
  stock_map = {}
  try:
    headers = {"X-API-Key": BUNNY_API_KEY}
    res = requests.get(BUNNY_PRODUCTS_URL, headers=headers, timeout=8)
    if res.status_code == 200:
      data = res.json()
      for item in data.get("products", []):
        try:
          prod_id = int(item.get("id"))
          stock_val = item.get("stock_count", item.get("stock", 0))
          stock_map[prod_id] = int(stock_val)
        except:
          pass
  except Exception as e:
    print(f"Stock fetch error: {e}")
  return stock_map


try:
  bot.delete_webhook(drop_pending_updates=True)
except Exception:
  pass


@bot.message_handler(commands=["start"])
def send_welcome(message):
  show_main_menu(message.chat.id, message.from_user.first_name)


def show_main_menu(chat_id, first_name="USER"):
  deposit_awaiting_amt.discard(chat_id)
  active_deposits.pop(chat_id, None)
  balance = user_balances.get(chat_id, 0.0)
  lang = user_languages.get(chat_id, "EN")

  markup = types.InlineKeyboardMarkup()
  if lang == "UR":
    markup.add(
        types.InlineKeyboardButton(
            "🛍️ مصنوعات (PRODUCTS)", callback_data="shop_menu"
        )
    )
    markup.row(
        types.InlineKeyboardButton(
            f"😃 پروفाइल ({balance:.2f} $)", callback_data="profile"
        ),
        types.InlineKeyboardButton(
            "💰 رقم جمع کریں (DEPOSIT)", callback_data="wallet"
        ),
    )
    markup.row(
        types.InlineKeyboardButton("🧾 آرڈر ہسٹری", callback_data="history"),
        types.InlineKeyboardButton("🎧 لائیو سپورٹ", callback_data="support"),
    )
    markup.row(
        types.InlineKeyboardButton(
            "🌐 زبان (LANGUAGE)", callback_data="lang"
        ),
        types.InlineKeyboardButton("🔗 API سیٹنگز", callback_data="api"),
    )
    welcome_text = (
        f"👑 **IMROOZ VIP STORE MEIN KHUSH AMDEED** 👑\n\n"
        f"سلام {str(first_name).upper()}! 🚀\n\n"
        f"💳 **آپ کا بیلنس:** `{balance:.2f} USDT`\n"
        "⚡ **بائنانس پے کم از کم 0.5 USDT سسٹم**\n\n"
        "👇 نیچے دیے گئے مینو سے سلیکٹ کریں:"
    )
  else:
    markup.add(types.InlineKeyboardButton("🛍️ PRODUCTS", callback_data="shop_menu"))
    markup.row(
        types.InlineKeyboardButton(
            f"😃 PROFILE ({balance:.2f} $)", callback_data="profile"
        ),
        types.InlineKeyboardButton(
            "💰 DEPOSIT (TOP-UP)", callback_data="wallet"
        ),
    )
    markup.row(
        types.InlineKeyboardButton("🧾 ORDER HISTORY", callback_data="history"),
        types.InlineKeyboardButton("🎧 LIVE SUPPORT", callback_data="support"),
    )
    markup.row(
        types.InlineKeyboardButton("🌐 LANGUAGE", callback_data="lang"),
        types.InlineKeyboardButton("🔗 API SETTINGS", callback_data="api"),
    )
    welcome_text = (
        f"👑 **WELCOME TO IMROOZ VIP STORE** 👑\n\n"
        f"HELLO {str(first_name).upper()}, WELCOME TO YOUR PREMIUM DIGITAL"
        f" STORE! 🚀\n\n"
        f"💳 **YOUR WALLET BALANCE:** `{balance:.2f} USDT`\n"
        "⚡ **BINANCE PAY MINIMUM 0.5 USDT SYSTEM**\n\n"
        "👇 PLEASE SELECT AN OPTION FROM THE MENU BELOW:"
    )

  bot.send_message(
      chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown"
  )


def send_menu_with_image(chat_id, image_key, text, markup):
  image_path = IMAGES.get(image_key)
  if image_path and os.path.exists(image_path):
    try:
      with open(image_path, "rb") as photo:
        bot.send_photo(
            chat_id,
            photo,
            caption=text,
            reply_markup=markup,
            parse_mode="Markdown",
        )
    except Exception:
      bot.send_message(
          chat_id, text, reply_markup=markup, parse_mode="Markdown"
      )
  else:
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
  chat_id = call.message.chat.id

  try:
    bot.delete_message(chat_id, call.message.message_id)
  except Exception:
    pass

  if call.data == "shop_menu":
    deposit_awaiting_amt.discard(chat_id)
    active_deposits.pop(chat_id, None)
    live_stocks = get_live_stock_map()
    markup = types.InlineKeyboardMarkup()

    for key, item in PRODUCTS.items():
      prod_id = item["id"]
      stock = live_stocks.get(prod_id, 0)
      if stock > 0:
        btn_text = f"{item['base_label']} (IN STOCK {stock})"
      else:
        btn_text = f"{item['base_label']} (OUT OF STOCK)"
      markup.add(types.InlineKeyboardButton(btn_text, callback_data=key))

    markup.add(
        types.InlineKeyboardButton(
            "🔙 BACK TO MAIN MENU", callback_data="back_main"
        )
    )
    shop_text = (
        "🛍️ **IMROOZ VIP STORE — AVAILABLE STOCK**\n\nSELECT A PRODUCT TO"
        " PURCHASE INSTANTLY USING YOUR BALANCE:"
    )
    send_menu_with_image(chat_id, "shop", shop_text, markup)

  elif call.data == "profile":
    deposit_awaiting_amt.discard(chat_id)
    active_deposits.pop(chat_id, None)
    balance = user_balances.get(chat_id, 0.0)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰 DEPOSIT FUNDS", callback_data="wallet"))
    markup.add(types.InlineKeyboardButton("🔙 BACK", callback_data="back_main"))

    profile_text = (
        f"👤 **VIP USER PROFILE**\n\n"
        f"🆔 USER ID: `{chat_id}`\n"
        f"💵 CURRENT BALANCE: **{balance:.2f} USDT**\n"
        f"💎 STATUS: VERIFIED VIP RESELLER"
    )
    send_menu_with_image(chat_id, "profile", profile_text, markup)

  elif call.data == "wallet":
    deposit_awaiting_amt.add(chat_id)
    balance = user_balances.get(chat_id, 0.0)

    msg = (
        f"💰 **DEPOSIT / TOP-UP (BINANCE PAY)** 💰\n\n"
        f"💵 **CURRENT BALANCE:** `{balance:.2f} USDT`\n\n"
        f"⚠️ **NOTE:** MINIMUM DEPOSIT LIMIT IS **0.5 USDT**.\n\n"
        f"👇 **STEP 1:** PLEASE TYPE AND SEND YOUR DEPOSIT AMOUNT IN CHAT (E.G.,"
        f" `0.5`, `1` OR `5`)."
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔙 CANCEL / BACK", callback_data="back_main")
    )
    send_menu_with_image(chat_id, "wallet", msg, markup)

  elif call.data == "history":
    deposit_awaiting_amt.discard(chat_id)
    active_deposits.pop(chat_id, None)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 BACK", callback_data="back_main"))
    send_menu_with_image(
        chat_id,
        "history",
        "🧾 **ORDER HISTORY**\n\nYOUR ORDERS ARE DELIVERED INSTANTLY AND"
        " AUTOMATICALLY.",
        markup,
    )

  elif call.data == "support":
    deposit_awaiting_amt.discard(chat_id)
    active_deposits.pop(chat_id, None)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 BACK", callback_data="back_main"))
    send_menu_with_image(
        chat_id,
        "support",
        "🎧 **CUSTOMER SUPPORT**\n\nCONTACT: @Imrokhan21",
        markup,
    )

  elif call.data == "lang":
    deposit_awaiting_amt.discard(chat_id)
    active_deposits.pop(chat_id, None)
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_EN"),
        types.InlineKeyboardButton("🇵🇰 اردو (Urdu)", callback_data="set_lang_UR"),
    )
    markup.row(
        types.InlineKeyboardButton("🇻🇳 Tiếng Việt", callback_data="set_lang_VI"),
        types.InlineKeyboardButton("🇨🇳 中文", callback_data="set_lang_ZH"),
    )
    markup.row(
        types.InlineKeyboardButton("🇪🇸 Español", callback_data="set_lang_ES"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_RU"),
    )
    markup.row(
        types.InlineKeyboardButton("🇮🇳 हिन्दी", callback_data="set_lang_HI"),
        types.InlineKeyboardButton("🇹🇭 ไทย", callback_data="set_lang_TH"),
    )
    markup.add(
        types.InlineKeyboardButton(
            "🔙 BACK TO MAIN MENU", callback_data="back_main"
        )
    )

    lang_text = "Chọn ngôn ngữ / Select language / 选择语言 / انتخاب زبان :"
    send_menu_with_image(chat_id, "lang", lang_text, markup)

  elif call.data.startswith("set_lang_"):
    chosen_lang = call.data.replace("set_lang_", "")
    user_languages[chat_id] = chosen_lang
    bot.answer_callback_query(call.id, text="Language updated successfully!")
    show_main_menu(chat_id)

  elif call.data == "back_main":
    show_main_menu(chat_id)

  elif call.data in PRODUCTS:
    deposit_awaiting_amt.discard(chat_id)
    active_deposits.pop(chat_id, None)
    item = PRODUCTS[call.data]
    live_stocks = get_live_stock_map()
    stock = live_stocks.get(item["id"], 0)

    if stock == 0:
      markup = types.InlineKeyboardMarkup()
      markup.add(
          types.InlineKeyboardButton(
              "🔙 BACK TO PRODUCTS", callback_data="shop_menu"
          )
      )
      bot.send_message(
          chat_id,
          f"⚠️ SORRY! **{item['name']}** IS CURRENTLY OUT OF STOCK.",
          reply_markup=markup,
          parse_mode="Markdown",
      )
      return

    balance = user_balances.get(chat_id, 0.0)
    needed = item["selling_price"]

    if balance < needed:
      diff = needed - balance
      markup = types.InlineKeyboardMarkup()
      markup.add(
          types.InlineKeyboardButton(
              "💰 DEPOSIT FUNDS NOW", callback_data="wallet"
          )
      )
      markup.add(
          types.InlineKeyboardButton(
              "🔙 BACK TO PRODUCTS", callback_data="shop_menu"
          )
      )
      msg = (
          f"⚠️ **INSUFFICIENT BALANCE!**\n\n"
          f"📦 ITEM: **{item['name']}**\n"
          f"💵 PRICE: **{needed} USDT**\n"
          f"💳 YOUR BALANCE: **{balance:.2f} USDT**\n\n"
          f"👉 YOU NEED TO DEPOSIT AN ADDITIONAL **{diff:.2f} USDT**."
      )
      bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")
      return

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            f"✅ YES, BUY NOW ({needed} USDT)",
            callback_data=f"confirm_{call.data}",
        )
    )
    markup.add(
        types.InlineKeyboardButton("🔙 CANCEL", callback_data="shop_menu")
    )

    bot.send_message(
        chat_id,
        f"🛒 **CONFIRM PURCHASE**\n\n"
        f"📦 **PRODUCT:** {item['name']}\n"
        f"💵 **PRICE:** {needed} USDT\n"
        f"💳 **CURRENT BALANCE:** {balance:.2f} USDT\n\n"
        f"REMAINING BALANCE AFTER PURCHASE WILL BE:"
        f" **{(balance - needed):.2f} USDT**.",
        reply_markup=markup,
        parse_mode="Markdown",
    )

  elif call.data.startswith("confirm_"):
    prod_key = call.data.replace("confirm_", "")
    if prod_key not in PRODUCTS:
      return

    item = PRODUCTS[prod_key]
    balance = user_balances.get(chat_id, 0.0)
    price = item["selling_price"]

    if balance < price:
      bot.send_message(
          chat_id, "❌ INSUFFICIENT BALANCE! PLEASE DEPOSIT FUNDS FIRST."
      )
      return

    bot.send_message(
        chat_id, "⏳ PROCESSING ORDER, FETCHING STOCK FROM SUPPLIER..."
    )

    headers = {"X-API-Key": BUNNY_API_KEY}
    payload_order = {
        "product_id": item["id"],
        "quantity": 1,
        "selling_price": price,
    }

    try:
      supplier_res = requests.post(
          BUNNY_ORDER_URL, json=payload_order, headers=headers, timeout=20
      )
      supp_data = supplier_res.json()

      if (
          supplier_res.status_code == 200
          and supp_data.get("status") == "success"
      ):
        user_balances[chat_id] = round(balance - price, 2)

        order_info = supp_data.get("order", {})
        delivered_data = order_info.get("delivered_item", "N/A")
        warranty = order_info.get("warranty_info", "ACTIVE")

        success_msg = (
            f"🎉 **ORDER DELIVERED SUCCESSFULLY!** 🎉\n\n"
            f"📦 **PRODUCT:** {item['name']}\n"
            f"🔑 **ACCOUNT / STOCK LINK:**\n`{delivered_data}`\n\n"
            f"🛡️ **WARRANTY INFO:** {warranty}\n"
            f"💵 **REMAINING BALANCE:** {user_balances[chat_id]:.2f} USDT\n\n"
            f"🌟 THANK YOU FOR USING IMROOZ VIP STORE!"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🛍️ SHOP MORE", callback_data="shop_menu")
        )
        markup.add(
            types.InlineKeyboardButton("🔙 MAIN MENU", callback_data="back_main")
        )
        bot.send_message(
            chat_id, success_msg, reply_markup=markup, parse_mode="Markdown"
        )
      else:
        err = supp_data.get("message", "SUPPLIER BALANCE OR STOCK ISSUE.")
        bot.send_message(
            chat_id,
            f"⚠️ ORDER COULD NOT BE DELIVERED: `{err}`\nYOUR BALANCE WAS NOT"
            " DEDUCTED.",
        )
    except Exception as e:
      bot.send_message(
          chat_id,
          "⚠️ DELIVERY API CONNECTION ISSUE. PLEASE CONTACT ADMIN:"
          " @Imrokhan21",
      )


@bot.message_handler(func=lambda msg: True)
def handle_all_messages(message):
  chat_id = message.chat.id
  text = message.text.strip()

  if chat_id in deposit_awaiting_amt:
    deposit_awaiting_amt.discard(chat_id)
    try:
      base_amt = float(text)

      if base_amt < 0.5:
        bot.reply_to(
            message,
            "❌ MINIMUM DEPOSIT LIMIT IS **0.5 USDT**! PLEASE ENTER 0.5 OR"
            " MORE. CLICK 'DEPOSIT' AGAIN.",
        )
        return

      bn_code = f"BN{random.randint(100000000000000, 999999999999999)}"
      exact_amount = round(base_amt, 2)

      active_deposits[chat_id] = exact_amount

      invoice_text = (
          f"💳 **USDT DEPOSIT INVOICE** 💳\n\n"
          f"📌 **CODE:** `{bn_code}` (FOR TRACKING ONLY, MEMO NOT REQUIRED)\n\n"
          f"🔹 **OPTION 1: BINANCE PAY (INSTANT, FREE)**\n"
          f"BINANCE ID: `{BINANCE_PAY_ID}`\n"
          f"AMOUNT: `{exact_amount:.2f}`\n\n"
          f"📌 **INSTRUCTIONS:**\n"
          f"OPEN BINANCE PAY -> SEND TO ID WITH THE EXACT AMOUNT ABOVE!\n"
          f"(AFTER PAYMENT, SEND YOUR BINANCE ORDER ID / TXID HERE)."
      )
      markup = types.InlineKeyboardMarkup()
      markup.add(
          types.InlineKeyboardButton("🔙 CANCEL / BACK", callback_data="back_main")
      )
      bot.send_message(
          chat_id, invoice_text, reply_markup=markup, parse_mode="Markdown"
      )

    except ValueError:
      bot.reply_to(
          message,
          "❌ PLEASE ENTER A VALID NUMBER (E.G., `0.5` OR `1`). CLICK 'DEPOSIT'"
          " AGAIN.",
      )

  elif chat_id in active_deposits:
    expected = active_deposits.pop(chat_id)
    bot.reply_to(
        message,
        f"✅ **DEPOSIT REQUEST SUBMITTED!**\n\nYOUR ORDER ID / TXID (`{text}`)"
        f" AND EXPECTED AMOUNT (`{expected:.2f} USDT`) HAVE BEEN"
        f" RECORDED.\nYOUR BALANCE WILL BE CREDITED AFTER ADMIN APPROVAL!",
    )
    show_main_menu(chat_id)


print("💎 IMROOZ VIP STORE (MULTI-LANGUAGE + @Imrokhan21) IS LIVE...")
bot.infinity_polling(skip_pending=True)
