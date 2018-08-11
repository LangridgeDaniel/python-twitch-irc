FROM alpine:3.7 as build

RUN \
	apk --update add python3 && \
  pip3 install setuptools wheel

COPY . /usr/local/app/service/
WORKDIR /usr/local/app/service

ENTRYPOINT [ "python3", "setup.py", "sdist", "bdist_wheel" ]


########################################################################################################################
# Test Container                                                                                                       #
########################################################################################################################
FROM build AS test

RUN \
  python3 setup.py sdist bdist_wheel && \
	pip3 install nose2 dist/*

ENTRYPOINT [ "nose2", "-c", "nose2.cfg" ]
