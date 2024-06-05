import os
import uuid
import asyncio
from aiogram import types, Router, F
from aiogram.filters import Command
from app.speech import recognise, convert_voice
from app.gpt import gpt_clear

router = Router()

@router.message(Command('start'))
async def handle_start(message: types.Message):
    await message.answer("Вас приветствует тех поддержка строительной компании O2 Development!\nМенеджер ответит на все ваши вопросы")


@router.message(F.voice)
async def handle_voice(message: types.Message):
    filename = str(uuid.uuid4())
    file_name_full = f"./voice/{filename}.ogg"
    file_name_full_converted = f"./ready/{filename}.wav"
    
    try:
        file_info = await message.bot.get_file(message.voice.file_id)
        await message.bot.download_file(file_info.file_path, file_name_full)
    except Exception as e:
        print(f"Ошибка при скачивании файла: {e}")
        await message.answer("Ошибка при скачивании файла. Пожалуйста, попробуйте ещё раз.")
        return
    
    convert_voice(file_name_full, file_name_full_converted)
    
    if os.path.exists(file_name_full_converted):
        print("Файл успешно создан:", file_name_full_converted)
        text = recognise(file_name_full_converted)
        print(f"Recognized text: {text}")
    else:
        print("Файл не создан:", file_name_full_converted)
        text = "Ошибка создания файла. Пожалуйста, попробуйте ещё раз."
    
    response = await gpt_clear(text)
    await message.answer(response)


@router.message(F.text)
async def handle_text(message: types.Message):
    user_text = message.text
    response = await gpt_clear(user_text)
    await message.answer(response)
