import os
import uuid
from aiogram.types import FSInputFile
from gtts import gTTS
from aiogram import types, Router, F
from aiogram.filters import Command
from app.speech import recognise, convert_voice
from app.gpt import gpt_clear

router = Router()

@router.message(Command('start'))
async def handle_start(message: types.Message):
    await message.answer("Вас приветствует Hilma Pro!")


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
    print('CHAT GPT: ',response)

    audio_filename = f"./ready/{filename}.mp3"
    tts = gTTS(response, lang='ru')
    tts.save(audio_filename)
    
    if os.path.exists(audio_filename):
        audio = FSInputFile(audio_filename)
        await message.answer_voice(audio)
        os.remove(audio_filename)
    else:
        await message.answer("Ошибка при создании аудиофайла. Пожалуйста, попробуйте ещё раз.")


@router.message(F.text)
async def handle_text(message: types.Message):
    user_text = message.text
    print('USER: ', user_text)
    response = await gpt_clear(user_text)
    print('CHAT GPT: ', response)
    await message.answer(response)
