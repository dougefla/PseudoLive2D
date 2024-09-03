# PseudoLive2D
This is a project for [Doctoral Exercise](https://yatani.jp/teaching/doku.php?id=grad-hands-on:start).

This repository's video part is modified based on [LivePortrait](https://github.com/KwaiVGI/LivePortrait).

## Introduction
This repository contains the code for our project, PseudoLive2D, which is a tool to generate Live2D-like animations with voice, from a reference character image, a driving video, and a voice audio.

## Prerequisites
- Docker
- Nvidia GPU

## Installation
1. Clone this repository
```
git clone https://github.com/dougefla/PseudoLive2D.git
cd PseudoLive2D
```
2. Build the docker image
```
docker build -t pseudolive2d:dev .
```
3. Download the pretrained model from [Google Drive](https://drive.google.com/drive/folders/1UtKgzKjFAOmZkhNK-OYT0caJ_w2XAnib), and Unzip and place them in `./pretrained_weights`. Make sure the directory structure is like [this](https://github.com/KwaiVGI/LivePortrait/blob/main/assets/docs/directory-structure.md)
4. Run the docker container. Here we bind the current directory to `/workspace` in the container, so that files are shared between the host and the container.
```
docker run --gpus all -it -v ${PWD}:/workspace pseudolive2d:dev
```
5. Now you should be in the docker container. You can run the following command to test the code.
```
python inference.py -s assets/examples/source/s0.jpg -d assets/examples/driving/d0.mp4
```
There might be several ONNXRuntimeError errors, but you can ignore them.
6. Check the results in `animations` folder in your host machine.

## Usage
### Data Preparation
- In the host machine, run the following command to record a video of yourself. Your head should keep fixed in the first several seconds. And avoid too much head movement. OpenCV and camera are needed: `pip install opencv-python`. Press `q` to stop recording.
```
python tools/auto_cut.py
```
### Inference
- Run the following command in the docker container to generate the animation.
```
python inference.py -s assets/examples/source/s0.jpg -d video_clips
```
- Change the source image and driving video by modifying the `-s` and `-d` arguments.
- You can get the results in the `animations` folder in the host machine.

## Code Explaination
- `inference.py`: The main script for inference.
- `src/live_portait_pipeline.py`: This is the most important file. It contains the input processing, motion model extraction, animation, etc.
  - `make_safe_motion_template`: This function is added by me, to make the motion template more stable.
  - If we do any thing, like extract any information from the video part, we should do it here, or in `inference.py`.

# TODO
- [ ] Currently, for clips, the model will load multiple times for each clip. We should modify the code to load the model only once, and keep the model in memory.
- [ ] Add voice support.
