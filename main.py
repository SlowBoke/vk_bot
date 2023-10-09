# -*- coding: utf-8 -*-

from acces_token import token
from random import randint
import vk_api
import vk_api.bot_longpoll
from log_config import main_log


class VkBot:
    group_id = 222488942

    def __init__(self, access_token):
        self.token = access_token
        self.vk = vk_api.VkApi(token=self.token)
        self.vk_methods = self.vk.get_api()
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(vk=self.vk, group_id=self.group_id, wait=25)

    def run(self):
        for event in self.long_poller.listen():
            main_log.info('Bot gets an event.')
            if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
                from_text = event.object.message['text']
                main_log.info("Bot gets an user's message.")
                self.vk_methods.messages.send(
                    user_id=event.object.message['from_id'],
                    random_id=randint(0, 2 ** 20),
                    message=f'Йоу, мистер Уайт. Твоё сообщение - "{from_text}"'
                )
                main_log.info('Bot sends message back to user.')
            else:
                main_log.info(f"Bot can't handle type of the current event: {event.type}")


if __name__ == '__main__':
    vk_bot = VkBot(access_token=token)
    vk_bot.run()
