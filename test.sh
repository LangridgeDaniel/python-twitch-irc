#!/usr/bin/env bash
set -ex

docker build -t python-twitch-irc-tests \
  --target test .

docker run --rm python-twitch-irc-tests -vvv
