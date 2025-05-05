import telebot
import os
import yt_dlp
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

api_key = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(api_key)

#inilinebutton



@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "به ربات دانلود یوتیوب خوش آمدید!\nلطفاً لینک ویدیوی یوتیوب را بفرستید.")

@bot.message_handler()
def dyt(message):
    text = message.text
    print(text)
   
    url = text

    try:
        ytt = {}

        with yt_dlp.YoutubeDL(ytt) as dlp:
            info = dlp.extract_info(url, download=False)
            te = info['url']
            butt = InlineKeyboardButton(text="button" , url=te)
            buty = InlineKeyboardMarkup(row_width=1)
            buty.add(butt)
            bot.send_message(message.chat.id , "download link" , reply_markup=buty)
    except Exception as e:
        print(e)

bot.polling(skip_pending=True)
