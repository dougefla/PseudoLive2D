# PseudoLive2D
This is a project for [Doctoral Exercise](https://yatani.jp/teaching/doku.php?id=grad-hands-on:start).

This repository's video part is modified based on [LivePortrait](https://github.com/KwaiVGI/LivePortrait).

## Introduction
This repository contains

## Prerequisites
- Docker
- Nvidia GPU

## Installation
1. Clone this repository
'''
git clone https://github.com/dougefla/PseudoLive2D.git && cd PseudoLive2D
'''
2. Build the docker image
'''
docker build -t pseudolive2d:dev .
'''
3. Run the docker container
'''
docker run --gpus all -it --rm -v $(pwd):/workspace pseudolive2d:dev
'''
