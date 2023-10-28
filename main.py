# -*- coding: utf-8 -*-

import handlers
import settings
import peewee
import db
from random import randint
from vk_api import VkApi
from log_config import main_log
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

try:
    from settings import TOKEN, GROUP_ID
except ImportError:
    exit('Do cp settings.py.default to settings.py and set token and group_id')


def db_init():
    """Initialising the database"""
    database = peewee.SqliteDatabase('db\\db.db')
    db.database_proxy.initialize(database)

    database.create_tables([db.UserState, db.Registration], safe=True)


class VkBot:
    """
    Echo bot for the vk.com

    Used Python3.11
    """

    def __init__(self, access_token, group_id):
        """
        :param access_token: secret token from the group in which the bot is implemented
        :param group_id: id of that group
        """
        self.token = access_token
        self.group_id = group_id
        self.vk = VkApi(token=self.token)
        self.vk_methods = self.vk.get_api()
        self.long_poller = VkBotLongPoll(vk=self.vk, group_id=self.group_id, wait=25)

    def run(self):
        """Running the bot"""
        db_init()
        for event in self.long_poller.listen():
            main_log.info('Bot gets an event.')
            self.event_handler(event=event)

    def message_new_event(self, event):
        user_id = event.object.message['peer_id']
        text = event.object.message['text']

        states = db.UserState.select()
        for state in states:
            if user_id == state.user_id:
                text_to_send = self.continue_scenario(user_id=user_id, text=text)
                break
        else:
            for intent in settings.INTENTS:
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(user_id=user_id, scenario_name=intent['scenario'])
                    break
            else:
                text_to_send = settings.DEFAULT_ANSWER
        return text_to_send

    def start_scenario(self, user_id, scenario_name):
        scenario = settings.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        cur_step = scenario['steps'][first_step]
        text_to_send = cur_step['text']
        db.UserState.create(
            user_id=user_id,
            scenario_name=scenario_name,
            step_name=first_step,
            context={}
        )
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = db.UserState.select().where(db.UserState.user_id == user_id).get()
        steps = settings.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]

        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                state.step_name = step['next_step']
            else:
                db.Registration.create(name=state.context['name'], email=state.context['email'])
                db.UserState.delete().where(db.UserState.user_id == user_id).execute()
        else:
            text_to_send = step['failure_text'].format(**state.context)
        state.save()
        return text_to_send

    def event_handler(self, event):
        """
        Defines event's type and handles it respectively

        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            text_to_send = self.message_new_event(event=event)
            main_log.info("Bot gets an user's message.")
            self.vk_methods.messages.send(
                user_id=event.object.message['from_id'],
                random_id=randint(0, 2 ** 20),
                message=text_to_send
            )
            main_log.info('Bot sends message back to user.')
        else:
            main_log.info(f"Bot can't handle type of the current event: {event.type}")


if __name__ == '__main__':
    vk_bot = VkBot(access_token=TOKEN, group_id=GROUP_ID)
    vk_bot.run()
