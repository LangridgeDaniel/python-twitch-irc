#!/usr/bin/env bash
set -ex

# export TWINE_REPOSITORY_URL=https://pypi.org/

docker build -t python-twitch-irc-release \
  --target release .

docker run --rm \
  -v ${PWD}/dist:/dist \
  -e TWINE_USERNAME \
  -e TWINE_PASSWORD \
  python-twitch-irc-release /dist/*
