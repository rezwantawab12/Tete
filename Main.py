import telebot
import os
import yt_dlp
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

api_key = os.environ("BOT_TOKEN")
bot = telebot.TeleBot(api_key)

uurl = {}  # ذخیره لینک و فرمت‌های هر کاربر

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "به ربات دانلود یوتیوب خوش آمدید!\nلطفاً لینک ویدیوی یوتیوب را بفرستید.")

@bot.message_handler()
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()
    print(chat_id, text)

    # مرحله 1: دریافت لینک
    if "youtube.com" in text or "youtu.be" in text:
        try:
            ydl_opts = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=False)
                formats = info.get('formats', [])

                # فقط کیفیت‌های ویدیویی با صدا را لیست می‌کنیم
                qualities = {}
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        height = f.get('height')
                        if height:
                            qualities[f"{height}p"] = f['url']

                if not qualities:
                    bot.send_message(chat_id, "هیچ کیفیت قابل دسترس نیست!")
                    return

                uurl[chat_id] = qualities

                # دکمه‌ها برای انتخاب کیفیت
                markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                for q in sorted(qualities.keys()):
                    markup.add(KeyboardButton(q))
                bot.send_message(chat_id, "لطفاً کیفیت را انتخاب کنید:", reply_markup=markup)

        except Exception as e:
            bot.send_message(chat_id, f"خطا در پردازش لینک: {e}")

    # مرحله 2: انتخاب کیفیت
    elif chat_id in uurl and text in uurl[chat_id]:
        direct_link = uurl[chat_id][text]
        button = InlineKeyboardButton(text="لینک دانلود مستقیم", url=direct_link)
        markup = InlineKeyboardMarkup().add(button)
        bot.send_message(chat_id, "لینک دانلود آماده است:", reply_markup=markup)
        del uurl[chat_id]

    else:
        bot.send_message(chat_id, "لطفاً ابتدا لینک یوتیوب بفرستید.")
        
bot.polling(skip_pending=True)
