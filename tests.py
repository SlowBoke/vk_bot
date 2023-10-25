# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch, Mock

from main import VkBot


class Test1(TestCase):
    def test_vkbot_run(self):
        count = 5
        obj = {'kek': 101}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('main.vk_api.VkApi'):
            with patch('main.vk_api.bot_longpoll.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = VkBot('', '')
                bot.event_handler = Mock()
                bot.run()

                bot.event_handler.assert_called()
                bot.event_handler.assert_any_call(event=obj)
                assert bot.event_handler.call_count == count
