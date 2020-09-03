FROM python:3.8-alpine

# Upgrade and install basic Python dependencies.
RUN apk upgrade --update \
  && apk add --no-cache bash perl jq zip git curl wget openssl ca-certificates sed openssh-client gcc \
  && update-ca-certificates \
  && apk add --no-cache --virtual .build-deps bzip2-dev libc-dev libffi-dev musl-dev \
  && pip install --upgrade pip setuptools six \
  && pip install --no-cache-dir gevent==1.5a2 flask==1.0.2 \
  && pip install awscli aws-sam-cli \
  && apk del .build-deps


ENV FLASK_PROXY_PORT 8080

RUN mkdir -p /actionProxy/owplatform
ADD actionproxy.py /actionProxy/
ADD owplatform/__init__.py /actionProxy/owplatform/
ADD owplatform/knative.py /actionProxy/owplatform/
ADD owplatform/openwhisk.py /actionProxy/owplatform/

ADD . /action
#ADD stub.sh /action/exec
#RUN chmod +x /action/exec

CMD ["/bin/bash", "-c", "cd actionProxy && python -u actionproxy.py"]
