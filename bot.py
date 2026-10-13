import telebot

TOKEN = '8961049217:AAFWq408kt2YdNPORU-tXfc7X5L2c7PzKFg'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 7055191372

user_ids = set()

products_stock = {
    'Zoom Pro 28D': '4.0 USDT (Out of Stock)',
    'Canva Pro Edu 1Y': '1.5 USDT (Out of Stock)',
    'Super Duolingo 1Y': '3.0 USDT (Out of Stock)',
    'Spotify 3M Link': '2.0 USDT (Out of Stock)',
    'Surfshark VPN 2M': '3.0 USDT (Out of Stock)',
    'NordVPN 3M Acc': '4.5 USDT (Out of Stock)',
    'Amazon Prime 1M': '2.0 USDT (Out of Stock)',
    'CapCut Pro 1M': '2.7 USDT (In Stock 24)',
    'Gemini Pro 18M': '1.5 USDT (In Stock 407)',
    'CapCut Pro 7D': '0.9 USDT (Out of Stock)',
    'Muse AI 2B Tokens': '3.3 USDT (Out of Stock)',
    'Crunchyroll 1M Link': '2.0 USDT (In Stock)',
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_ids.add(message.chat.id)
  bot.reply_to(
      message,
      'Khush amdeed! Current stock check karne ke liye /stock command use'
      ' karein.',
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
  for prod, status in products_stock.items():
    catalog_text += f'• {prod} – {status}\n'
  bot.reply_to(message, catalog_text, parse_mode='Markdown')


print('Bot chal raha hai...')
bot.infinity_polling()
