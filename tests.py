# -*- coding: utf-8 -*-
from copy import deepcopy

import peewee

import handlers
import settings, main
from unittest import TestCase
from unittest.mock import patch, Mock
from vk_api.bot_longpoll import VkBotMessageEvent

from image_generator import generate_ticket
from main import VkBot


db = main.db_init()


class Test1(TestCase):
    RAW_EVENT = {
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
                bot.send_image = Mock()
                bot.run()

                bot.event_handler.assert_called()
                bot.event_handler.assert_any_call(event=obj)
                assert bot.event_handler.call_count == count

    INPUTS = [
        'йоу',
        'Привет',
        'А когда?',
        'Где будет РобоФест?',
        'Зарегай меня',
        'Мишима Кадзуя',
        'адрес hell@swip',
        'simple_dimple@gmail.com',
        'Спасибки, помог',
        'Досвидос',
    ]

    EXTRACTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        settings.INTENTS[1]['answer'],
        settings.INTENTS[2]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='Мишима Кадзуя',
                                                                            email='simple_dimple@gmail.com'),
        settings.INTENTS[4]['answer'],
        settings.INTENTS[5]['answer']
    ]

    # @db.atomic()
    def test_vkbot_event_handler(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        image_mock = Mock()

        with patch('handlers.generate_ticket_handler', return_value=image_mock):
            with patch('main.VkBotLongPoll', return_value=long_poller_mock):
                bot = VkBot('', '')
                bot.vk_methods = api_mock
                bot.send_image = Mock()
                bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        assert real_outputs == self.EXTRACTED_OUTPUTS

    def test_image_generation(self):
        with open('files\\test_avatar.png', 'rb') as avatar_file:
            avatar_mock = Mock()
            avatar_mock.content = avatar_file.read()

        with patch('requests.get', return_value=avatar_mock):
            ticket_file = generate_ticket('Попыт', 'simpledimple@gmail.com')

        with open('files\\test_ticket.png', 'rb') as expected_file:
            expected_bytes = expected_file.read()

        assert ticket_file.read() == expected_bytes

