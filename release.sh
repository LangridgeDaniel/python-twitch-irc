#!/usr/bin/env bash
set -ex

export TWINE_REPOSITORY_URL=https://pypi.org/legacy/

# twine upload --repository-url https://test.pypi.org/legacy/ dist/*

docker build -t twitch-irc-release \
  --target release .

docker run --rm \
  -v ${PWD}/dist:/dist \
  -e TWINE_USERNAME \
  -e TWINE_PASSWORD \
  -e TWINE_REPOSITORY_URL \
  twitch-irc-release /dist/*
