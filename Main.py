import telebot
import yt_dlp
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


api_key = ("7801225750:AAEqJnAvQgGI7pXXKemNkW3yp4qrdz1JOIU")
bot = telebot.TeleBot(api_key)


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "سلام! لینک ویدیوی یوتیوب را بفرستید تا لینک دانلود برایتان ساخته شود.")

@bot.message_handler(func=lambda message: True)
def download_youtube(message):
    url = message.text
    print("لینک دریافت شده:", url)

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'skip_download': True,
            'cookiefile': 'cookies.txt',  # فایل کوکی کنار اسکریپت باشد
        }

        with yt_dlp.YoutubeDL(ydl_opts) as dlp:
            info = dlp.extract_info(url, download=False)
            video_url = info.get('url')

        # ساخت دکمه برای لینک دانلود
        button = InlineKeyboardButton(text="دانلود ویدیو", url=video_url)
        markup = InlineKeyboardMarkup().add(button)

        bot.send_message(message.chat.id, "لینک دانلود ویدیو آماده است:", reply_markup=markup)

    except Exception as e:
        print("خطا:", e)
        bot.send_message(message.chat.id, "خطا در دریافت لینک! احتمالاً باید کوکی‌ها به‌روز شوند یا لینک نامعتبر است.")

bot.polling(skip_pending=True)
