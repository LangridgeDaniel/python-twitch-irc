#!/usr/bin/env bash
set -ex

# build container
docker build -t twitch-irc-build \
  --target build .

mkdir -p dist

# build into build
docker run --rm -v ${PWD}/dist:/build twitch-irc-build --dist-dir /build
