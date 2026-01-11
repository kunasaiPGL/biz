import os
import telebot
from openai import OpenAI

# Эти строчки берут твои секретные ключи из настроек Render, а не из текста кода
TG_TOKEN = os.getenv('TG_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')

bot = telebot.TeleBot(TG_TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    # Приветствие в твоем стиле
    bot.reply_to(message, "Yo, check it! Я Hoodepzy, твой AI-стилист из гетто. Какой аутфит ищем сегодня, homie?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Инструкция для ИИ (System Prompt), чтобы он базарил как надо
    system_prompt = ""Ты — Hoodepzy, премиальный AI-стилист. Твоя задача — давать четкие, экспертные рекомендации по стилю и одежде. Ты общаешься вежливо, профессионально и по существу, но не как робот, а как элитный консультант. Твоя экспертиза охватывает все мировые стили: от минимализма Кремниевой долины до высокой моды Европы. Ты не используешь сленг, только чистый, уверенный английский. Твоя цель — помочь клиенту найти его уникальный образ и предоставить лучшие ссылки на товары с платформ вроде 1688 или Alibaba. Будь краток, точен и авторитетен.""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices.message.content)
    except Exception as e:
        bot.reply_to(message, "Сорри, бро, че-то мозги заклинило. Попробуй позже.")
        print(e)

if __name__ == "__main__":
    print("Hoodepzy is alive...")
    bot.infinity_polling()
