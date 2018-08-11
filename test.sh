#!/usr/bin/env bash
set -ex

docker build -t twitch-irc-tests \
  --target test .

docker run --rm twitch-irc-tests -vvv
