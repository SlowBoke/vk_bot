# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import patch, Mock

from main import VkBot


event = {
    'group_id': 222488942,
    'type': 'message_new',
    'event_id': 'c20a08d9098dd212cd586598ad84dd27f43586fe',
    'v': '5.131',
    'object': {
        'message': {
            'entity_version': 0,
            'date': 1698328326,
            'from_id': 308611803,
            'id': 41,
            'out': 0,
            'attachments': [],
            'conversation_message_id': 39,
            'fwd_messages': [],
            'important': False,
            'is_hidden': False,
            'peer_id': 308611803,
            'random_id': 0,
            'text': 'Кек'
        },
        'client_info': {
            'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link',
                               'open_photo', 'callback', 'intent_subscribe', 'intent_unsubscribe'],
            'keyboard': True,
            'inline_keyboard': True,
            'carousel': True,
            'lang_id': 0
        }
    }
}

class Test1(TestCase):
    def test_vkbot_run(self):
        count = 5
        obj = {'kek': 101}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('main.VkApi'):
            with patch('main.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = VkBot('', '')
                bot.event_handler = Mock()
                bot.run()

                bot.event_handler.assert_called()
                bot.event_handler.assert_any_call(event=obj)
                assert bot.event_handler.call_count == count

    def test_vkbot_event_handler(self):
        event = None


        with patch('main.VkApi'):
            with patch('main.VkBotLongPoll'):
                pass
