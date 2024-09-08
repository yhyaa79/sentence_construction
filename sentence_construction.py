import telebot
from telebot import types
import json
from g4f.client import Client
import time

API_TOKEN = "7276619998:AAEjuXMmkO2HkUjnnWvZNbQlP5I-1KNqkO0"
bot = telebot.TeleBot(API_TOKEN)


def chat_with_gpt(user_id, text_chatGPT_35_turbo):
    try:
        system_message = {
            "role": "system",
            #"content": "شما یک دستیار هوشمند و دوستانه هستید که پاسخ‌ها را به زبان فارسی و با دقت و احترام و بطور خیلی خلاصه ارائه می‌دهید. توجه داشته باشید که برخی کلمات ممکن است در زبان محاوره معانی متفاوتی داشته باشند. از زمینه و استفاده‌های رایج میان مردم برای درک و پاسخ‌گویی به این نوع کلمات استفاده کنید و سعی کنید پاسخی ارائه دهید که با معنی متداول در زبان روزمره هماهنگ باشد."
            "content": "شما یک دستیار هوشمند برای کمک به افراد ناشنوا هستید. تمام پاسخ‌ها باید به زبان فارسی ساده و قابل فهم ارائه شوند. تحت هیچ شرایطی از کلمات یا عبارات انگلیسی یا زبان‌های دیگر استفاده نکنید. پاسخ‌ها باید خلاصه و فقط شامل کلمات فارسی باشند."
        }
        user_message = {"role": "user", "content": text_chatGPT_35_turbo}

        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[system_message, user_message],  # Only current conversation messages
            temperature=0.5,  # Adjusts creativity vs accuracy
            max_tokens=50,   # Limits the response length
            top_p=0.9,        # Controls diversity of responses
            frequency_penalty=0.5,  # Reduces repetition
            presence_penalty=0.6     # Encourages new topic introduction
        )

        model_reply = response.choices[0].message.content
        return model_reply
    except Exception as e:
        print(f"An error occurred: {e}")
        return "متاسفانه یک خطا رخ داده است، لطفا دوباره تلاش کنید."


def meaning_word(user_id, word):
    description = "لطفا معنی کلمه زیر را بطور کامل برام توضیح بده"
    return chat_with_gpt(user_id, f"{description}\n{word}")


def correction_sentence(user_id, sentence):
    description = "لطفا جمله زیر رو برام تصحیح کن"
    return chat_with_gpt(user_id, f"{description}\n{sentence}")


texe_start = """این بات ساخته شده است تا مثل یک مربی به افراد ناشنوا برای درک کردن معنی کلمه ها و به تصحیح کردن جمله ها کمک کنه.

لطفا توضیحات را مطالعه کنید و بعد گزینه "start" را انتخاب کنید تا وارد قسمت اصلی بات شوید.

با انتخاب گزینه "start" شما وارد پنل اصلی برنامه می شوید و دو گزینه 'معنی کلمه' و 'تصحیح جمله' وجود دارد.

با انتخاب گزینه 'معنی کلمه' میتوانید کلمه مورد نظر خود را بفرستید و بعد از چند ثانیه بات معنی کلمه شما رو براتون میفرسته.

با انتخاب گزینه 'تصحیح جمله' میتوانید جمله مورد نظر خود را بفرستید و بعد از چند ثانیه بات جمله تصحیح شده شما رو براتون میفرسته.

گاهی ممکنه بات دچار مشکل بشه و در این صورت با تایپ یا انتخاب /start بات دوباره شروع به کار میکنه.




ایدی سازنده بات : @yah_ya_suo

"""


@bot.message_handler(commands=['start', 'reset'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn_start = types.KeyboardButton('Start')
    markup.add(itembtn_start)
    bot.send_message(message.chat.id, "به بات خوش آمدید! یک گزینه را انتخاب کنید:", reply_markup=markup)




@bot.message_handler(func=lambda message: message.text == 'Start')
def show_options(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('معنی کلمه')
    itembtn2 = types.KeyboardButton('تصحیح جمله')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "یک گزینه را انتخاب کنید:", reply_markup=markup)



@bot.message_handler(func=lambda message: message.text == 'معنی کلمه')
def option_meaning_word(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn_back = types.KeyboardButton('برگشت')
    markup.add(itembtn_back)
    bot.send_message(message.chat.id, "لطفا کلمه مورد نظر خود را وارد کنید یا گزینه 'برگشت' انتخاب کنید:", reply_markup=markup)
    bot.register_next_step_handler(message, process_meaning_word)


def process_meaning_word(message):
    if message.text == 'برگشت':
        show_options(message)
    else:
        user_id = message.from_user.id
        word = message.text
        bot.send_message(message.chat.id, "لطفا صبر کنید...")
        try:
            response = meaning_word(user_id, word)
            bot.send_message(message.chat.id, response)
        except Exception as e:
            print(f"Error processing meaning word: {e}")
            bot.send_message(message.chat.id, "دوباره تلاش کنید.")
        option_meaning_word(message)  # Prompt user again


@bot.message_handler(func=lambda message: message.text == 'تصحیح جمله')
def option_correction_sentence(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn_back = types.KeyboardButton('برگشت')
    markup.add(itembtn_back)
    bot.send_message(message.chat.id, "لطفا جمله مورد نظر خود را وارد کنید یا گزینه 'برگشت' انتخاب کنید:", reply_markup=markup)
    bot.register_next_step_handler(message, process_correction_sentence)


def process_correction_sentence(message):
    if message.text == 'برگشت':
        show_options(message)
    else:
        user_id = message.from_user.id
        sentence = message.text
        bot.send_message(message.chat.id, "لطفا صبر کنید...")
        try:
            response = correction_sentence(user_id, sentence)
            bot.send_message(message.chat.id, response)
        except Exception as e:
            print(f"Error processing correction sentence: {e}")
            bot.send_message(message.chat.id, "دوباره تلاش کنید.")
        option_correction_sentence(message)  # Prompt user again


while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        time.sleep(5)  # Wait a few seconds before restarting
