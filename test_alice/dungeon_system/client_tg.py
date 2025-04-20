import json
import logging
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from game_master import get_dm_answer

logging.basicConfig(level=logging.INFO)

# TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TOKEN = "7644370360:AAHGfBBJQ3xJuI2h3WkGa1JOXoRCgwL2wqs"
bot = Bot(token=TOKEN)
dp = Dispatcher()

class ChatState(StatesGroup):
    active = State()

class FeedbackState(StatesGroup):
    waiting_for_rating = State()
    waiting_for_comment = State()

active_chats = {}

def save_to_json(user_data: dict):
    try:
        with open('conversations.json', 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(user_data)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        with open('conversations.json', 'w', encoding='utf-8') as f:
            json.dump([user_data], f, ensure_ascii=False, indent=2)

@dp.message(Command('start'))
async def start_chat(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    if user_id in active_chats or await state.get_state() is not None:
        await message.answer("Пожалуйста, завершите текущий диалог перед началом нового.")
        return
    
    await state.set_state(ChatState.active)
    active_chats[user_id] = []
    await message.answer("Привет! О чем вы хотите историю и какой длины? Напишите ваш запрос:")

@dp.message(ChatState.active)
async def handle_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in active_chats:
        await message.answer("Используйте /start для начала нового диалога.")
        return
    
    active_chats[user_id].append({"role": "user", "content": message.text})
    
    try:
        # Отправляем статус "печатает"
        await bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING
        )
        
        updated_history = get_dm_answer(active_chats[user_id])
        active_chats[user_id] = updated_history
        
        last_message = updated_history[-1]['content']
        builder = InlineKeyboardBuilder()
        builder.button(text="⏹️ Прекратить разговор", callback_data="stop_chat")
        
        # Отправка с Markdown-форматированием
        await message.answer(
            last_message,
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("Произошла ошибка при обработке запроса.")

@dp.callback_query(F.data == "stop_chat")
async def stop_chat(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if user_id not in active_chats:
        await callback.answer("Диалог уже завершен")
        return
    
    chat_history = active_chats.pop(user_id)
    await state.set_state(FeedbackState.waiting_for_rating)
    await state.update_data(chat_history=chat_history)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="👍 Понравилось", callback_data="feedback_like")
    builder.button(text="👎 Не понравилось", callback_data="feedback_dislike")
    await callback.message.answer("Оцените, пожалуйста, ваш диалог:", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("feedback_"))
async def handle_feedback(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    await state.update_data(rating=action)
    
    if action == "dislike":
        await state.set_state(FeedbackState.waiting_for_comment)
        await callback.message.answer("Пожалуйста, напишите, что именно вам не понравилось:")
    else:
        data = await state.get_data()
        user_data = {
            "user_id": callback.from_user.id,
            "timestamp": datetime.now().isoformat(),
            "history": data['chat_history'],
            "rating": data['rating'],
            "comment": None
        }
        save_to_json(user_data)
        await state.clear()
        await callback.message.answer("Спасибо за оценку! Вы можете начать новый диалог с /start")

@dp.message(FeedbackState.waiting_for_comment)
async def handle_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_data = {
        "user_id": message.from_user.id,
        "timestamp": datetime.now().isoformat(),
        "history": data['chat_history'],
        "rating": data['rating'],
        "comment": message.text
    }
    save_to_json(user_data)
    await state.clear()
    await message.answer("Спасибо за ваш отзыв! Вы можете начать новый диалог с /start")

if __name__ == '__main__':
    dp.run_polling(bot)