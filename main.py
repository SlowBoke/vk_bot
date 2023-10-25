# -*- coding: utf-8 -*-


from random import randint
import vk_api
import vk_api.bot_longpoll
from log_config import main_log

try:
    from settings import TOKEN, GROUP_ID
except ImportError:
    exit('Do cp settings.py.default to settings.py and set token and group_id')


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
        self.vk = vk_api.VkApi(token=self.token)
        self.vk_methods = self.vk.get_api()
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(vk=self.vk, group_id=self.group_id, wait=25)

    def run(self):
        """Running the bot"""
        for event in self.long_poller.listen():
            main_log.info('Bot gets an event.')
            self.event_handler(event=event)

    def event_handler(self, event):
        """
        Defines event's type and handles it respectively

        :param event: VkBotMessageEvent object
        :return: None
        """
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
    vk_bot = VkBot(access_token=TOKEN, group_id=GROUP_ID)
    vk_bot.run()
