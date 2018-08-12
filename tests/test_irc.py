import unittest
from unittest import mock

from python_twitch_irc import TwitchIrc


class Dummy:
    pass


class TestIrcClient(unittest.TestCase):
    def test_cleared_chat(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.command = 'CLEARCHAT'
        message.params = ['#test-room']
        message.tags = {
            'ban-duration': '600',
            'room-id': '36026978',
            'target-user-id': '244083199',
            'tmi-sent-ts': '1533676810932',
        }

        with mock.patch.object(TwitchIrc, 'on_cleared_chat') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_cleared_chat to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(isinstance(args[1], dict), "Expect tags to be dictionary")
            self.assertTrue(args[1]['ban-duration'] == message.tags['ban-duration'], "Expect field from tags")
            self.assertTrue(args[2] == message.params[0], "Expect argument to be channel")

    def test_channel_ban(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.command = 'CLEARCHAT'
        message.params = ['#test-room', 'test_user']
        message.tags = {
            'ban-duration': '600',
            'room-id': '36026978',
            'target-user-id': '244083199',
            'tmi-sent-ts': '1533676810932',
        }

        with mock.patch.object(TwitchIrc, 'on_channel_ban') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_channel_ban to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(isinstance(args[1], dict), "Expect tags to be dictionary")
            self.assertTrue(args[1]['ban-duration'] == message.tags['ban-duration'], "Expect field from tags")
            self.assertTrue(args[2] == message.params[0], "Expect argument to be channel")
            self.assertTrue(args[3] == message.params[1], "Expected argument to be username")

    def test_on_hosting(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.command = 'HOSTTARGET'
        message.params = ['#host-user', 'hostee 2']
        message.tags = {}

        with mock.patch.object(TwitchIrc, 'on_hosting') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_hosting to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(args[1] == 'host-user', "Expect argument to be hosting user")
            self.assertTrue(args[2] == 'hostee', "Expect argument to be hostee")
            self.assertTrue(args[3] == 2, "Expect argument to be viewers")

    def test_on_stop_hosting(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.command = 'HOSTTARGET'
        message.params = ['#host-user', '- 2']
        message.tags = {}

        with mock.patch.object(TwitchIrc, 'on_stop_hosting') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_stop_hosting to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(args[1] == 'host-user', "Expect argument to be hosting user")
            self.assertTrue(args[2] == 2, "Expect argument to be viewers")

    def test_on_notice(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.command = 'NOTICE'
        message.params = ['#test-room', 'This room is now in slow mode. You may send messages every 120 seconds.']
        message.tags = {
            'msg-id': 'slow_on',
        }

        with mock.patch.object(TwitchIrc, 'on_notice') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_notice to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(isinstance(args[1], dict), "Expect tags to be dictionary")
            self.assertTrue(args[1]['msg-id'] == message.tags['msg-id'], "Expect field from tags")
            self.assertTrue(args[2] == message.params[0], "Expect argument to be channel")
            self.assertTrue(args[3] == message.params[1], "Expect argument to be message")

    def test_on_roomstate(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.command = 'ROOMSTATE'
        message.params = ['#test-room']
        message.tags = {
            'room-id': '36026978',
            'rituals': '0',
            'emote-only': '0',
        }

        with mock.patch.object(TwitchIrc, 'on_roomstate') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_roomstate to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(isinstance(args[1], dict), "Expect tags to be dictionary")
            self.assertTrue(args[1]['room-id'] == message.tags['room-id'], "Expect field from tags")
            self.assertTrue(args[2] == message.params[0], "Expect argument to be channel")

    def test_on_usernotice(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.command = 'USERNOTICE'
        message.params = ['#test-room']
        message.tags = {
            'badges': 'subscriber/12,bits/100',
            'display-name': 'Test_User',
        }

        with mock.patch.object(TwitchIrc, 'on_usernotice') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_usernotice to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(isinstance(args[1], dict), "Expect tags to be dictionary")
            self.assertTrue(args[1]['badges'] == message.tags['badges'], "Expect field from tags")
            self.assertTrue(args[2] == message.params[0], "Expect argument to be channel")
            self.assertTrue(not args[3], "Expect no message")

    def test_on_userstate(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.command = 'USERSTATE'
        message.params = ['#test-room']
        message.tags = {
            'badges': 'subscriber/12,bits/100',
            'display-name': 'Test_User',
        }

        with mock.patch.object(TwitchIrc, 'on_userstate') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_userstate to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(isinstance(args[1], dict), "Expect tags to be dictionary")
            self.assertTrue(args[1]['badges'] == message.tags['badges'], "Expect field from tags")
            self.assertTrue(args[2] == message.params[0], "Expect argument to be channel")

    def test_on_whisper(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.source = 'a_user!a_user@a_user.tmi.twitch.tv'
        message.command = 'WHISPER'
        message.params = ['test_user', 'message']
        message.tags = {
            'badges': 'subscriber/12,bits/100',
            'display-name': 'Test_User',
        }

        with mock.patch.object(TwitchIrc, 'on_whisper') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_whisper to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(isinstance(args[1], dict), "Expect tags to be dictionary")
            self.assertTrue(args[1]['badges'] == message.tags['badges'], "Expect field from tags")
            self.assertTrue(args[2] == 'a_user', "Expect argument to be a user")
            self.assertTrue(args[3] == message.params[1], "Expect argument be message")

    def test_on_privmsg(self):
        irc = TwitchIrc('dummy', 'dummy_token')
        message = Dummy()
        message.source = 'a_user!a_user@a_user.tmi.twitch.tv'
        message.command = 'PRIVMSG'
        message.params = ['#test-room', 'message']
        message.tags = {
            'badges': 'subscriber/12,bits/100',
            'display-name': 'Test_User',
        }

        with mock.patch.object(TwitchIrc, 'on_message') as mocked:
            irc._on_handle_twitch(message)

            # grab call list
            args, kwargs = mocked.call_args_list[0]

            # Assertions
            self.assertTrue(mocked.called, "Expect on_message to be called")
            self.assertTrue(isinstance(args[0], int), "Expect timestamp to be an integer")
            self.assertTrue(isinstance(args[1], dict), "Expect tags to be dictionary")
            self.assertTrue(args[1]['badges'] == message.tags['badges'], "Expect field from tags")
            self.assertTrue(args[2] == message.params[0], "Expect argument be a channel")
            self.assertTrue(args[3] == 'a_user', "Expect argument be a user")
            self.assertTrue(args[4] == message.params[1], "Expect argument to be a message")
