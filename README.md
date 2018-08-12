# python-twitch-irc
`python-twitch-irc` is a layer of logic which takes the [Pydle] package and provides (or modifies existing) logic to handle Twitch IRC pecularities.

## Installation
`python-twitch-irc` can be installed via `pip install python-twitch-irc`

## Usage
`python-twitch-irc` is a layer which sits above `Pydle` so if documentation is lacking, refer to `Pydle` documentation.  Twitch IRC is not fully compliant with RFC1459 and later, so some behaviors may not function as expected (such as who/whois, nick, etc).

### Twitch
Utilizing this library requires a Twitch account and a token generated for that account.  A token can be generated via [TwitchApps].  Note that the generated token has the prefix 'oauth' which should be removed before use.

#### Rate Limiting
`TwitchIrc` does not provide rate limiting.  To see rates and limits, see [Twitch Irc Guide].

### Basic Usage
`TwitchIrc` is expected to be used as a base class.
```python
from python_twitch_irc import TwitchIrc

# Simple echo bot.
class MyOwnBot(TwitchIrc):
    def on_connect(self):
         self.join('#best_streamer')

    # Override from base class
    def on_message(self, timestamp, tags, channel, user, message):
        self.message(channel, message)

client = MyOwnBot('MyBot', 'MyTwitchOAuthToken').start()
client.handle_forever()
```
### Pydle IRC Functionality
Most of the Basic IRC functionality can be found via [Pydle Documentation].  It shold be noted that not all functionality provided by `Pydle` is compatible with Twitch IRC.  

### Twitch IRC functionality
`TwitchIrc` provides the following additional functionality.  These functions may or may not require permissioning per channel.
``` python
def start(self):
  # Starts the connection the Twitch IRC servers

def stop(self):
  # Stops connection to Twitch IRC servers

def whisper(self, user, message):
  # Sends a whisper to a user

def message(self, target, message):
  # Sends a message to a channel or whisper to a user

def action(self, target, message):
  # Performs the IRC '<username> ACTION'
  # * John slaps Jim around a bit with a large trout

def timeout(self, channel, user, seconds, reason=None):
  # Times a user out for specified seconds from a channel

def ban(self, channel, user, reason=None):
  # Permanently bans a user from a channel

def unban(self, channel, user):
  # Unbans a user from a channel

def slow(self, channel, seconds):
  # Sets the message rate of a channel to specified seconds

def slow_off(self, channel):
  # Turns off slowmode

def followers(self, channel, restrict):
  # Sets a channel to follower mode only.  Restrict should be set to values as
  # defined here: https://help.twitch.tv/customer/portal/articles/659095-chat-moderation-commands

def followers_off(self, channel):
  # Turns off follower mode in a channel

def subscribers(self, channel):
  # Turns on subscriber mode in a channel

def subscribers_off(self, channel):
  # Turns off subscriber mode in a channel

def clear(self, channel):
  # Clears the chat history in a channel

def r9kbeta(self, channel):
  # Turns on r9kbeta mode in a channel

def r9kbeta_off(self, channel):
  # Turns off r9kbeta mode in a channel

def emoteonly(self, channel):
  # Turns on emote only mode in a channel

def emoteonly_off(self, channel):
  # Turns off emote only mode in a channel

def commercial(self, channel, seconds=30):
  # Runs a commercial in the channel.  Seconds should be an appropriate value
  # defined here: https://help.twitch.tv/customer/portal/articles/659095-chat-moderation-commands

def host(self, channel, target):
  # Hosts a channel

def unhost(self, channel):
  # Stops hosting a channel

def mod(self, channel, user):
  # Gives moderation powers to user in channel

def unmod(self, channel, user):
  # Removes moderation powers from user in channel
```
### Twitch IRC Callbacks
`TwitchIRC` provides callbacks which can be overriden.  Their purpose/meaning can be divined from [Twitch Irc Guide].
```python
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
```

### Capabilities
By default, capabilities are enabled.  To disable capabilities, override the following functions and return `False`:
``` python
def on_capability_twitch_tv_membership_available(self, value):
def on_capability_twitch_tv_tags_available(self, value):
def on_capability_twitch_tv_commands_available(self, value):
```
## Development
Development environment utilizes `docker` and `docker-compose` for building and testing the library.
### Building
The `python_twitch_irc` library can be build via `./build.sh`
### Testing
The unit tests can be run via `./test.sh`.  Local changes can be tested without rebuilding the test container via `./test-dev.sh` but requires that the initial test container be built.

[Pydle]: <https://github.com/Shizmob/pydle>
[Pydle Documentation]: <http://pydle.readthedocs.io/en/latest/api/features.html#rfc1459>
[TwitchApps]: <https://twitchapps.com/tmi/>
[Twitch Irc Guide]: <https://dev.twitch.tv/docs/irc/guide>
