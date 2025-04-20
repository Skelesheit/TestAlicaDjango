import asyncio
import threading

from asgiref.sync import sync_to_async

from test_alice import commands
from test_alice.consts import THEMES
from test_alice.dungeon_system.game_master import get_dm_answer
from test_alice.models import ChatHistory, Session


class AliceGameService:
    async def get_completion(self, user_id: str, message="") -> str:
        session = await commands.get_or_create_session(user_id)

        # Первое сообщение — приветствие
        if await commands.check_session(user_id) and message == "":
            return self.start_message()

        # Если думаем — отдаём точки
        if session.thinking:
            session.waiting_step += 1
            await sync_to_async(session.save)()
            return "." * (session.waiting_step % 4 or 1)

        # Иначе запускаем генерацию
        await commands.write_message(session, message, role='user')
        session.thinking = True
        session.waiting_step = 1
        await sync_to_async(session.save)()

        self._start_llm_thread(session.id)

        return "."

    def start_message(self) -> str:
        return (
            f"Привет, это квест игра, генерируемая LLM, какой тематики хочешь квест?"
            f"{THEMES}"
        )

    def get_history(self, messages) -> list:
        return [{'role': message.role, 'content': message.message} for message in messages]

    def _start_llm_thread(self, session_id: int):
        def run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            session = loop.run_until_complete(sync_to_async(Session.objects.get)(id=session_id))
            messages = loop.run_until_complete(commands.get_messages_from_session(session))
            history = self.get_history(messages)
            answer = loop.run_until_complete(get_dm_answer(history))
            loop.run_until_complete(commands.write_message(session, answer, role='assistant'))

            session.thinking = False
            session.waiting_step = 0
            loop.run_until_complete(sync_to_async(session.save)())

        threading.Thread(target=run).start()