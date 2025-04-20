import subprocess
import os
import tempfile
from moviepy import VideoFileClip
from pysrt import SubRipFile, SubRipItem, SubRipTime
import re
from datetime import timedelta
from subtitle import gen_subtitles


def cut(input_path, output_path, start_time, end_time):
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start_time),
        '-to', str(end_time),
        '-i', input_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'fast',
        output_path
    ]

    subprocess.run(cmd)


def scale(path, output, width=None, height=None):
    cmd = [
        'ffmpeg', '-y',
        '-i', path,
        '-vf', f'scale={width if width is not None else "-1"}:{height if height is not None else "-1"}',
        output
    ]
    subprocess.run(cmd)


def border(input_path, output_path, border_hd=0, border_lr=0, border_color="black"):
    """
    Add border using FFmpeg (faster for large videos)
    :param border_color: Can be color name or hex code (#RRGGBB)
    :param border_hd: size of border under and upper of original video (total height increased on border_hd*2)
    :param border_lr: size of left and right border (total width increased on border_lr*2l)
    """
    cmd = [
        'ffmpeg', '-y',
        '-i', input_path,
        '-vf', f'pad=width=iw+{border_lr*2}:height=ih+{border_hd*2}:x={border_lr}:y={border_hd}:color={border_color}',
        '-c:a', 'copy',
        output_path
    ]

    subprocess.run(cmd)


def blur(input_path, output_path, blur_koeff=10):
    cmd = [
        'ffmpeg',
        '-y',
        '-i', input_path,
        '-vf', f'boxblur={blur_koeff}:5',
        '-c:a', 'copy',
        output_path
    ]
    subprocess.run(cmd, check=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.STDOUT)


def compose_center(background_path, overlay_path, output_path):
    cmd = [
        'ffmpeg', '-y',
        '-i', background_path,
        '-i', overlay_path,
        '-filter_complex',
        '[0:v][1:v]overlay=(W-w)/2:(H-h)/2',
        '-c:a', 'copy',
        output_path
    ]
    subprocess.run(cmd, check=True)


def crop(input_path, output_path, width, height, x, y):
    cmd = [
        'ffmpeg', '-y', '-i',
        input_path, '-vf',
        f'crop={width}:{height}:{x}:{y}',
        output_path
    ]

    subprocess.run(cmd, check=True)


def get_duration(input_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_path
    ]
    return float(subprocess.run(cmd, capture_output=True, text=True).stdout)


def to_vertical(input_path, output_path, w=1080, h=1920, background_path=None,
                bg_blur=10):
    """
    Duration of main and background videos must be equal.
    :param background: background video. If None then background is scaled blur video
    """
    width, height = VideoFileClip(input_path).size
    if (background_path is None):
        cmd = [
            'ffmpeg', '-y',
            '-i', input_path,
            '-vf',
            'split=2[bg][fg];'
            f'[bg]scale={w}:{h}:force_original_aspect_ratio=increase,'
            f'crop={w}:{h},boxblur={bg_blur}[bg];'
            f'[fg]scale={w}:-2[fg];'
            '[bg][fg]overlay=(W-w)/2:(H-h)/2',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'copy',
            output_path
        ]

        subprocess.run(cmd, check=True)
    else:
        temp_dir = os.path.dirname(output_path) or '.'
        temp = tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.mp4')
        fg_duration, bg_duration = get_duration(
            input_path), get_duration(background_path)
        if (bg_duration < fg_duration):
            raise 'Error: background video duration is\
                less than main video duration'
        if (bg_duration > fg_duration):
            cut(background_path, temp.name, 0, fg_duration)
        else:
            temp.name = background_path
        cmd = [
            'ffmpeg',
            '-y',
            '-i', temp.name,
            '-i', input_path,
            '-filter_complex',
            f'[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,'
            f'crop={w}:{h},boxblur={bg_blur}[bg];'
            f'[1:v]scale={w}:-2[fg];'
            '[bg][fg]overlay=(W-w)/2:(H-h)/2[v]',
            '-map', '[v]',
            '-map', '1:a?',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'copy',
            output_path
        ]

        subprocess.run(cmd, check=True)


def compile_subtitles(input_path, subtitles, output_path):
    cmd = ['ffmpeg', '-i',
           input_path, '-vf',
           f"subtitles={subtitles}:force_style='FontName=Roboto,Fontsize=18,PrimaryColour=&HFFFFFF&,BackColour=&H80000000&,OutlineColour=&H000000&,BorderStyle=4,Alignment=2,MarginV=30'",
           '-c:v', 'libx264', '-crf', '23',
           '-preset', 'fast',
           '-c:a', 'copy',
           output_path
           ]
    subprocess.run(cmd, check=True)


def make_shorts(input_path, output_path, start_time=0, end_time=None, background_path=None, bg_blur=10):
    temp_dir = os.path.dirname(output_path) or '.'
    cutted_video = tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.mp4')
    vert_video = tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.mp4')
    subtitle_file = tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.srt')

    if (end_time is None and start_time == 0):
        cutted_video.name = input_path
    else:
        if (end_time is None):
            end_time = get_duration(input_path)
        cut(input_path, cutted_video.name, start_time, end_time)

    to_vertical(cutted_video.name, vert_video.name,
                background_path=background_path, bg_blur=bg_blur)
    gen_subtitles(cutted_video.name, subtitle_file.name)
    compile_subtitles(vert_video.name, subtitle_file.name, output_path)

    cutted_video.close()
    vert_video.close()
    subtitle_file.close()
