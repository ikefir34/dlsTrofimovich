import telebot
import detection_model

bot = telebot.TeleBot("7815106284:AAGdmaRIEwBTY26PC_oincoAs2ICbNrqcwY")

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, "Скиньте в чат фотографии или видео для обработки")

@bot.message_handler(content_types=['photo'])
def photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)  # Берём первое фото (самое маленькое)
    downloaded_file  = bot.download_file(file_info.file_path)
    file_path = f"input/{file_info.file_path.split('/')[-1]}"
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    detection_model.img_processing(file_path)
    output_file = open("output/out_img.jpg", "rb")
    bot.send_photo(message.chat.id, output_file)

@bot.message_handler(content_types=['video'])
def video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = f"input/{message.video.file_name}"
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    detection_model.video_processing(file_path)
    output_file = open("output/out_vid.mp4", "rb")
    bot.send_video(message.chat.id, output_file)

bot.infinity_polling()