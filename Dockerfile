FROM alpine:3.7 AS build

RUN \
	apk --update add python3 && \
  pip3 install -U setuptools wheel

COPY . /usr/local/app/build
WORKDIR /usr/local/app/build

ENTRYPOINT [ "python3", "setup.py", "sdist", "bdist_wheel" ]


########################################################################################################################
# Test Container                                                                                                       #
########################################################################################################################
FROM build AS test

RUN \
  python3 setup.py bdist_wheel && \
	pip3 install nose2 dist/*

ENTRYPOINT [ "nose2", "-c", "nose2.cfg" ]


########################################################################################################################
# Release Container                                                                                                       #
########################################################################################################################
FROM build AS release
ARG TWINE_USERNAME
ARG TWINE_PASSWORD
ARG TWINE_REPOSITORY_URL

RUN \
	pip3 install -U twine

ENTRYPOINT [ "twine", "upload" ]
