 DEPOSIT INVOICE** 💳\n\n"
                f"📌 **CODE:** `{bn_code}` (FOR TRACKING ONLY, MEMO NOT REQUIRED)\n\n"
                f"🔹 **OPTION 1: BINANCE PAY (INSTANT, FREE)**\n"
                f"BINANCE ID: `{BINANCE_PAY_ID}`\n"
                f"AMOUNT: `{exact_amount:.2f}`\n\n"
                f"📌 **INSTRUCTIONS:**\n"
                f"OPEN BINANCE PAY -> SEND TO ID WITH THE EXACT AMOUNT ABOVE!\n"
                f"(AFTER PAYMENT, SEND YOUR BINANCE ORDER ID / TXID HERE)."
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔙 CANCEL / BACK", callback_data="back_main"))
            bot.send_message(chat_id, invoice_text, reply_markup=markup, parse_mode="Markdown")
            
        except ValueError
