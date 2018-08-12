#!/usr/bin/env bash
set -ex

# build container
docker build -t python-twitch-irc-build \
  --target build .

mkdir -p dist

# build into build
docker run --rm -v ${PWD}/dist:/usr/local/app/build/dist python-twitch-irc-build
