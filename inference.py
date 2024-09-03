# coding: utf-8
"""
for human
"""

import os
import os.path as osp
import tyro
import subprocess
from src.config.argument_config import ArgumentConfig
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from src.live_portrait_pipeline import LivePortraitPipeline


def partial_fields(target_class, kwargs):
    return target_class(**{k: v for k, v in kwargs.items() if hasattr(target_class, k)})


def fast_check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except:
        return False


def fast_check_args(args: ArgumentConfig):
    if not osp.exists(args.source):
        raise FileNotFoundError(f"source info not found: {args.source}")
    if not osp.exists(args.driving):
        raise FileNotFoundError(f"driving info not found: {args.driving}")

def main_stream():
    # set tyro theme
    tyro.extras.set_accent_color("bright_cyan")
    args = tyro.cli(ArgumentConfig)
    driving_root = args.driving
    args.driving = os.path.join(driving_root, f"clip_1.avi")
    i=1
    with open('mylist.txt', 'w') as f:
        f.write(f"file 'animations/test1--clip_{i}_concat.mp4'\n")
    while os.path.exists(args.driving):
        ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
        if osp.exists(ffmpeg_dir):
            os.environ["PATH"] += (os.pathsep + ffmpeg_dir)

        if not fast_check_ffmpeg():
            raise ImportError(
                "FFmpeg is not installed. Please install FFmpeg (including ffmpeg and ffprobe) before running this script. https://ffmpeg.org/download.html"
            )

        fast_check_args(args)

        # specify configs for inference
        inference_cfg = partial_fields(InferenceConfig, args.__dict__)
        crop_cfg = partial_fields(CropConfig, args.__dict__)

        live_portrait_pipeline = LivePortraitPipeline(
            inference_cfg=inference_cfg,
            crop_cfg=crop_cfg
        )

        # run, processed clip will be stored as test1--clip_i.mp4
        live_portrait_pipeline.execute(args)

        with open('mylist.txt', 'a') as f:
            f.write(f"file 'animations/test1--clip_{i}_concat.mp4'\n")
        i+=1
        args.driving = os.path.join(driving_root, f"clip_{i}.avi")

    # concate all clips
    subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "mylist.txt", "-c", "copy", "output.mp4"])


def main():
    # set tyro theme
    tyro.extras.set_accent_color("bright_cyan")
    args = tyro.cli(ArgumentConfig)

    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
    if osp.exists(ffmpeg_dir):
        os.environ["PATH"] += (os.pathsep + ffmpeg_dir)

    if not fast_check_ffmpeg():
        raise ImportError(
            "FFmpeg is not installed. Please install FFmpeg (including ffmpeg and ffprobe) before running this script. https://ffmpeg.org/download.html"
        )

    fast_check_args(args)

    # specify configs for inference
    inference_cfg = partial_fields(InferenceConfig, args.__dict__)
    crop_cfg = partial_fields(CropConfig, args.__dict__)

    live_portrait_pipeline = LivePortraitPipeline(
        inference_cfg=inference_cfg,
        crop_cfg=crop_cfg
    )

    # run
    live_portrait_pipeline.execute(args)


if __name__ == "__main__":
    main()
    # main_stream()
