import logging

import pendulum
import pydle

# Create a featurized client
BaseIrcClass = pydle.featurize(pydle.features.RFC1459Support, pydle.features.IRCv3Support)

# Set up logger
LOGGER = logging.getLogger()

# Constants
TWITCH_IRC_SERVER = 'irc.chat.twitch.tv'
TWITCH_IRC_PORT = 6667
MILLI_TO_SECONDS = 1000
TS_KEY = 'tmi-sent-ts'


class TwitchIrc(BaseIrcClass):
    def __init__(self, username, token, server=TWITCH_IRC_SERVER, port=TWITCH_IRC_PORT):
        self._username = username
        self._token = token
        self._server = server
        self._port = port

        # Instantiate inherited class
        super().__init__(
            self._username,
            [],
            username=self._username,
        )

    def start(self):
        super().connect(
            self._server,
            self._port,
            password=f"oauth:{self._token}",
        )

        return self

    def stop(self):
        self.disconnect(True)

    def whisper(self, user, message):
        """
        This seems super gimmicky, but so far this is the only way
        way I've seen to do this (at least through IRC).  It's definitely
        not documented.
        """
        if user[0] == '#':
            LOGGER.warning(f"Whisper is for users only.")
        else:
            super().message('#jtv', f".w {user} {message}")

    def message(self, target, message):
        if target[0] == '#':
            super().message(target, message)
        else:
            self.whisper(target, message)

    def action(self, target, message):
        if target[0] == '#':
            self.message(target, f"\x01ACTION {message}\x01")
        else:  # Again, gimmicky
            self.whisper(target, f"/me {message}")

    def timeout(self, channel, user, seconds, reason=None):
        reason = reason or ''

        self.message(channel, f".timeout {user} {seconds} {reason}")

    def ban(self, channel, user, reason=None):
        reason = reason or ''

        self.message(channel, f".ban {user} {reason}")

    def unban(self, channel, user):
        self.message(channel, f".unban {user}")

    def slow(self, channel, seconds):
        self.message(channel, f".slow {seconds}")

    def slow_off(self, channel):
        self.message(channel, ".slowoff")

    def followers(self, channel, restrict):
        self.message(channel, f".followers {restrict}")

    def followers_off(self, channel):
        self.message(channel, ".followersoff")

    def subscribers(self, channel):
        self.message(channel, ".subscribers")

    def subscribers_off(self, channel):
        self.message(channel, ".subscribersoff")

    def clear(self, channel):
        self.message(channel, f".clear")

    def r9kbeta(self, channel):
        self.message(channel, f".r9kbeta")

    def r9kbeta_off(self, channel):
        self.message(channel, f".r9kbetaoff")

    def emoteonly(self, channel):
        self.message(channel, f".emoteonly")

    def emoteonly_off(self, channel):
        self.message(channel, f".emoteonlyoff")

    def commercial(self, channel, seconds=30):
        self.message(channel, f".commercial {seconds}")

    def host(self, channel, target):
        self.message(channel, f".host {target}")

    def unhost(self, channel):
        self.message(channel, f".unhost")

    def mod(self, channel, user):
        self.message(channel, f".mod {user}")

    def unmod(self, channel, user):
        self.message(channel, f".unmod {user}")

    def on_unknown(self, message):
        self._on_handle_twitch(message)

    def _on_handle_twitch(self, message):
        cmd_to_func = {
            'CLEARCHAT': self.on_raw_twitch_clear_chat,
            'HOSTTARGET': self.on_raw_twitch_host_target,
            'RECONNECT': self.on_raw_twitch_reconnect_cmd,
            'ROOMSTATE': self.on_raw_twitch_roomstate,
            'USERNOTICE': self.on_raw_twitch_usernotice,
            'USERSTATE': self.on_raw_twitch_userstate,
            'WHISPER': self.on_raw_twitch_whisper,
            'NOTICE': self.on_raw_twitch_notice,
            'PRIVMSG': self.on_raw_twitch_privmsg,
        }

        try:
            funct = cmd_to_func[message.command]

            # Generate the timestamp if not included
            # in provided tags
            if TS_KEY in message.tags:
                ts = from_twitch_ts(message.tags[TS_KEY])
            else:
                ts = pendulum.now().int_timestamp

            # Call handler
            LOGGER.debug(f"{ts} {message.tags} {message.command} {message.params}")
            funct(ts, message)
        except KeyError:
            super().on_unknown(message)

    # Raw Capabilities
    def on_raw_twitch_clear_chat(self, timestamp, message):
        if len(message.params) > 1:
            self.on_channel_ban(timestamp, message.tags, message.params[0], message.params[1])
        else:
            self.on_cleared_chat(timestamp, message.tags, message.params[0])

    def on_raw_twitch_host_target(self, timestamp, message):
        host = message.params[0].split('#')[1]
        params = message.params[1].split()
        hostee = params[0]
        viewers = int(params[1]) if params[1] != '-' else 0

        if hostee == '-':
            self.on_stop_hosting(timestamp, host, viewers)
        else:
            self.on_hosting(timestamp, host, hostee, viewers)

    def on_raw_twitch_reconnect_cmd(self, timestamp, message):
        LOGGER.debug(f"RECONNECT command received {pendulum.from_timestamp(timestamp)}")

        # Call overrideable
        self.on_reconnect_cmd(timestamp)

    def on_raw_twitch_roomstate(self, timestamp, message):
        self.on_roomstate(
            timestamp,
            message.tags,
            message.params[0],
        )

    def on_raw_twitch_usernotice(self, timestamp, message):
        self.on_usernotice(
            timestamp,
            message.tags,
            message.params[0],
            message.params[1] if len(message.params) > 1 else '',
        )

    def on_raw_twitch_userstate(self, timestamp, message):
        self.on_userstate(
            timestamp,
            message.tags,
            message.params[0],
        )

    def on_raw_twitch_whisper(self, timestamp, message):
        self.on_whisper(
            timestamp,
            message.tags,
            parse_user(message.source),
            message.params[1],
        )

    def on_raw_twitch_notice(self, timestamp, message):
        self.on_notice(
            timestamp,
            message.tags,
            message.params[0],
            message.params[1],
        )

    def on_raw_twitch_privmsg(self, timestamp, message):
        self.on_message(
            timestamp,
            message.tags,
            message.params[0],
            parse_user(message.source),
            message.params[1],
        )

    # Capabilities
    # These cause the client to request the twitch capabilities
    def on_capability_twitch_tv_membership_available(self, value):
        return True

    def on_capability_twitch_tv_tags_available(self, value):
        return True

    def on_capability_twitch_tv_commands_available(self, value):
        return True

    # Raw IRC codes and commands
    def on_raw_004(self, msg):
        """
        Twitch IRC does not match what the pydle library expects
        which causes Pydle to raise exceptions.
        Override on_raw_004 and prevent super call
        """
        LOGGER.debug(f'on_raw_004: {msg}')

    def on_raw_421(self, message):
        """
        Twitch doesn't support WHO/WHOIS,
        so ignore errors from those commands
        """
        if message.params[1] in {'WHO', 'WHOIS'}:
            LOGGER.debug('Pydle sent WHO/WHOIS which resulted in 421')
        else:
            super().on_raw_421(message)

    def on_raw_notice(self, message):
        """
        NOTICE is technically a capabilities issue but
        Pydle does not return tags so override it and pass the
        arguments we want
        """
        self._on_handle_twitch(message)

    def on_raw_privmsg(self, message):
        """
        Pydle does not returns tags so override on_raw_privmsg
        without calling the super (as this client redefines on_message
        and calls would likely break everything)
        """
        self._on_handle_twitch(message)

    # Overrideables
    def on_cleared_chat(self, timestamp, tags, channel):
        pass

    def on_channel_ban(self, timestamp, tags, channel, user):
        pass

    def on_hosting(self, timestamp, host, hostee, viewers):
        pass

    def on_stop_hosting(self, timestamp, host, viewers):
        pass

    def on_notice(self, timestamp, tags, channel, message):
        pass

    def on_reconnect_cmd(self, timestamp):
        pass

    def on_roomstate(self, timestamp, tags, channel):
        pass

    def on_usernotice(self, timestamp, tags, channel, message):
        pass

    def on_userstate(self, timestamp, tags, channel):
        pass

    def on_whisper(self, timestamp, tags, user, message):
        pass

    def on_message(self, timestamp, tags, channel, user, message):
        pass


# Utility
def from_twitch_ts(ts):
    return int(ts) // MILLI_TO_SECONDS


def parse_user(source):
    return source.split('!')[0]
