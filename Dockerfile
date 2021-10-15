FROM python:3.8

ARG DOCKER_HOME="/opt/yijun"
ARG DOCKER_CODE="/opt/yijun/code"
ARG DOCKER_USER="yijun"
ARG DOCKER_UID=5000

RUN useradd -d ${DOCKER_HOME} -m -U -u ${DOCKER_UID} ${DOCKER_USER}

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

USER ${DOCKER_USER}

WORKDIR ${DOCKER_CODE}

ENV PYTHONPATH=.

COPY --chown=${DOCKER_USER} . .

CMD ["gunicorn", "app.patched:app", "--work-class", "gevent", "-w", "3", "-b", "0.0.0.0:8000"] 