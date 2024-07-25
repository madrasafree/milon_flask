FROM ubuntu:24.04

COPY requirements.txt /

WORKDIR /

# Install Python and any other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip libpq-dev && \
    apt-get install -y python3.12-venv && \
    apt-get clean

RUN python3 -m venv venv

RUN . venv/bin/activate && \
    pip3 install --upgrade pip && \
    pip install --no-cache-dir 'greenlet==3.0.3' setuptools 'SQLAlchemy==2.0.31' && \
    pip install --no-cache-dir 'cython<3.0.0' && \
    pip install --no-cache-dir --no-build-isolation 'pyyaml==5.4.1' && \
    pip install --no-cache-dir --no-input -r /requirements.txt \
