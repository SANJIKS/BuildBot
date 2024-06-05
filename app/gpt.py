import aiohttp
from decouple import config

OPENAI_KEY = config('OPENAI_KEY')
OPENAI_KEY2 = config('OPENAI_KEY2')
PROMPT = config('PROMPT')

async def gpt_clear(message):
    chat_history = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": f"Клиент: {message} | Менеджер:"}
    ]

    for token in (OPENAI_KEY2,):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    json={
                        "model": "gpt-4",
                        "messages": chat_history,
                        "temperature": 0.6
                    },
                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                ) as response:
                    response.raise_for_status()
                    data = await response.json()

            generated_text = data["choices"][0]["message"]["content"]

            try:
                generated_text = generated_text.split(':')[1]
            except:
                generated_text = generated_text

            components = generated_text.split(',')
            cleaned_components = [component.strip('\'"') for component in components]
            formatted_components = ', '.join(cleaned_components)

            return formatted_components
        except Exception as e:
            print(f"Ошибка с токеном {token}: {e}")

    raise Exception("Оба токена вызвали ошибку")
