# CUDA 12.1を含むPyTorch公式イメージ
# https://hub.docker.com/r/pytorch/pytorch/tags
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04
# Note: amd64向けのイメージなので、ARMベースのCPU（M1/M2/M3 Macなど）では警告が出ますが、動作には問題ありません。

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV HF_HOME="/root/.cache/huggingface"
ENV PYTHONPATH="/app:/app/src"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    python3.11-venv && \
    rm -rf /var/lib/apt/lists/*

# python3 -> python3.11 のシンボリックリンクを作成
RUN ln -s /usr/bin/python3.11 /usr/bin/python

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .

# Jupyter Labのインストール
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
