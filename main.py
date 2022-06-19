from moviepy.editor import VideoFileClip
from config import TOKEN
import datetime
import telebot

API_TOKEN = TOKEN

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Стартовый набор команд"""
    bot.reply_to(message, "Hi!\nSend to me a video.")


@bot.message_handler(content_types=['video'])
def get_file(message):
    """Преобразование видео в гифку"""
    today = datetime.datetime.today()
    time_now = today.strftime("%Y-%m-%d_%H-%M-%S")
    file_info = bot.get_file(message.video.file_id)
    bot.reply_to(message, "Благодарю, минуточку...")
    with open(f"videos/{time_now}_video.mp4", "wb") as f:
        file_content = bot.download_file(file_info.file_path)
        f.write(file_content)
    clip = VideoFileClip(f"videos/{time_now}_video.mp4")
    clip.write_gif(f"gifs/{time_now}_gif.gif", fps=15)
    bot.send_animation(message.chat.id, open(f"gifs/{time_now}_gif.gif", "rb"))


bot.infinity_polling()
