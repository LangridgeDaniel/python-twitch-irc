#!/usr/bin/env python3
from twitch_irc.irc import TwitchIrc
import logging
import string
import random
from threading import Thread
import time

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


def run_me(irc):
    irc.start()
    irc.handle_forever()


def main():
    tb = TwitchIrc(
        'cannibaljeebus',
        'k4iyz3b9s0xt2ethzesupkmv7d6wnb',
    )

    t = Thread(
        target=run_me,
        daemon=False,
        args=(tb,),
    )

    t.start()

    time.sleep(4)
    tb.join('#cannibaljeebus')

    tb.r9kbeta('#cannibaljeebus')
    time.sleep(1)
    tb.r9kbeta_off('#cannibaljeebus')
    time.sleep(1)
    tb.emoteonly('#cannibaljeebus')
    time.sleep(1)
    tb.emoteonly_off('#cannibaljeebus')
    time.sleep(1)
    tb.commercial('#cannibaljeebus')
    time.sleep(1)
    tb.host('#cannibaljeebus', 'likelyontilt')
    time.sleep(1)
    tb.unhost('#cannibaljeebus')
    time.sleep(1)
    tb.mod('#cannibaljeebus', 'potato_bot_reee')
    time.sleep(1)
    tb.unmod('#cannibaljeebus', 'potato_bot_reee')


if __name__ == '__main__':
    main()
