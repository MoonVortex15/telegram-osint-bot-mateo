import telebot
import requests

BOT_TOKEN = '9163446232:AAGpGLrx8fv0KVAbRk_OGNvwGG5DLXYgO1M'  # твой токен из @BotFather

API_BASE = 'https://osintclodcode.onrender.com/?num='

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Probiv Telegram OSINT Bot v0.1 (УКР + RU)\n\nКидай любой номер или @юзер\nЯ пробью ФИО, отчество родителей, группы, чаты и IP.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    bot.reply_to(message, f"🔍 Ищу данные по `{text}`... (может занять до 20 сек)")

    try:
        response = requests.get(API_BASE + text, timeout=30)
        data = response.json()

        results = data.get("results", [])
        if not results:
            bot.reply_to(message, "⚠️ Ничего не найдено. Возможно номер не поддерживается.")
            return

        final_text = f"📄 *OSINT RESULTS for {text}*\n\n"
        for item in results:
            final_text += f"{item}\n\n"

        bot.reply_to(message, final_text, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}\n\nПроверь токен и интернет.")

bot.polling(none_stop=True)
