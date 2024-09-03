# Use NVIDIA's CUDA base image
FROM pytorch/pytorch:2.4.0-cuda11.8-cudnn9-devel

# Update package lists and install necessary packages
RUN apt update && apt install -y \
    build-essential \
    curl \
    git \
    wget \
    ffmpeg \
    libsm6 \
    libxext6

# Copy your application code into the container
COPY . /app/LivePortrait
RUN pip install -r /app/LivePortrait/requirements.txt
