# This is the terminal client, to chat with the system.

from pprint import pprint

from test_alice.dungeon_system.game_master import get_dm_answer


initial_user_message = input("О чем вы хотите историю? Какой длины? >> ")

chat_history = [{"role":"user", "content": initial_user_message}]

while True:
    chat_history = get_dm_answer(chat_history)
    pprint(chat_history[-1]["content"])

    new_user_message = input(">>> ")

    if new_user_message == "exit":
        print("Exit detected")
        break

    chat_history.append({"role":"user", "content": new_user_message})