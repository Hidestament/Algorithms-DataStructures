FROM python:3.8.2-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    apt-utils \
    gcc \
    build-essential \
    && pip install --no-cache-dir \
    autopep8 \
    flake8 \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install numpy==1.18.2 && \
    pip install scipy==1.4.1 && \
    pip install scikit-learn==0.22.2.post1 && \
    pip install numba==0.48.0 && \
    pip install networkx==2.4