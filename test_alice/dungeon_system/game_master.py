from openai import OpenAI
# как-то я криво структуру проекта сделал, смотря откуда запускаешь, нужно по разному импортировать
import test_alice.dungeon_system.prompts as prompts
import test_alice.dungeon_system.config as config
# import prompts as prompts
# import config as config

from pprint import pprint

import random

client = OpenAI(
    base_url = config.base_url,
    api_key=config.key, # required, but unused
)


def write_story_plot(chat_history):
    random_theme = random.choice(prompts.THEMES)
    # Случайная тема будет использована если пользователь ничего не попросил конкретного, чтобы сделать LLM креативнее
    print(f"Random selected theme is: {random_theme}")
    completion = client.chat.completions.create(
    model=config.story_writer_model,
    messages=[
        {"role": "system", "content": prompts.PLOT_GENERATOR_SYSTEM_PROMPT.format(theme=random_theme)}, 
    ]  + chat_history, )

    answer = completion.choices[0].message.content
    print(answer)
    return answer

def get_dm_answer(chat_history):
    """
    Takes chat history as input, returns updated chat history.
    Chat history can be empty or can have only one message from user, where he asks for certain adventure theme.

    chat_history - list of dicts. Each dict is {Role: text}
    Roles are "user" and "assistant", also "system"
    """

    # Если это первое сообщение, и игра еще не началась
    if len(chat_history) < 2:
        plot = write_story_plot(chat_history)

        # Подставляем в промпт ведущего наш сгенерированный сюжет
        filled_prompt = prompts.DUNGEON_MASTER_SYSTEM_PROMPT_TEMPLATE.format(plot = plot)
        chat_history = [{"role": "system", "content": filled_prompt},]

    response = client.chat.completions.create(
        model=config.model,
        messages=chat_history )
    answer = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": answer})

    return chat_history
