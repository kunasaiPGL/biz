import os
import json
import requests

TG_TOKEN = os.getenv('TG_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')
BASE_URL = f"https://api.telegram.org/bot{TG_TOKEN}"

# System Prompt, чтобы бот общался по делу и профессионально
SYSTEM_PROMPT = "Ты — Hoodepzy, премиальный AI-стилист из гетто. Твоя задача — давать четкие, экспертные рекомендации по стилю и одежде. Общайся вежливо, профессионально и по существу, но не как робот. Твой стиль — уверенный и глобальный. Используй чистый, уверенный английский."

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

def get_openai_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("api.openai.com", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print(f"Error calling OpenAI: {response.text}")
        return "Сорри, бро, че-то мозги заклинило. Попробуй позже."

def lambda_handler(event, context):
    try:
        update = json.loads(event['body'])
        chat_id = update['message']['chat']['id']
        text = update['message']
        
        if text == '/start':
            send_message(chat_id, "Yo, check it! Я Hoodepzy, твой AI-стилист. Какой аутфит ищем сегодня?")
        else:
            response_text = get_openai_response(text)
            send_message(chat_id, response_text)
    except Exception as e:
        print(f"Error handling request: {e}")
        return {'statusCode': 200, 'body': 'OK'} # Возвращаем OK, чтобы Telegram не паниковал

    return {'statusCode': 200, 'body': 'OK'}
