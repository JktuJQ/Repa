import subprocess
import os
import tempfile
from moviepy import VideoFileClip

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
        '-vf', f'scale={width if width is not None else '-1'}:{height if height is not None else '-1'}',
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

def blur(input_path, output_path):
    temp_dir = os.path.dirname(output_path) or '.'
    with tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.mp4') as temp_file:
        cmd = [
            'ffmpeg',
            '-y',
            '-i', input_path,
            '-vf', 'boxblur=10:5',
            '-c:a', 'copy',
            temp_file.name
        ]
        subprocess.run(cmd, check=True, 
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
        
        # Only move to final location if successful
        os.replace(temp_file.name, output_path)
        return True

def compose_center(background_path, overlay_path, output_path):
    cmd = [
        'ffmpeg',
        '-i', background_path,
        '-i', overlay_path,
        '-filter_complex',
        '[0:v][1:v]overlay=(W-w)/2:(H-h)/2',
        '-c:a', 'copy',
        output_path
    ]
    subprocess.run(cmd)

def to_vertical(input_path, output_path, w=1080, h=1920, background=None,
                bg_blur=15, in_one_cmd=True):
    """
    :param background: background video. If None then background is scaled blur video
    """
    width, height = VideoFileClip(input_path).size
    if (background is None):
        if (in_one_cmd):
            cmd = [
            'ffmpeg', '-y',
            '-i', input_path,
            '-filter_complex',
            # Split into two streams
            f"[0:v]split[original][back];"
            
            # Process background stream
            f"[back]scale=iw*{w}:{h},boxblur={bg_blur}[bg];"
            
            # Process foreground stream
            f"[original]scale={w}:-1[fg];"
            
            # Composite
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2[out]",
            
            '-map', '[out]',
            '-map', '0:a?',  # Keep original audio if exists
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'copy',
            '-y',
            output_path
            ]

            subprocess.run(cmd, check=True)
        else:
            temp_dir = os.path.dirname(output_path) or '.'
            stdscaled = tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.mp4')
            blur_bkg = tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.mp4')
            bkg = tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.mp4')
            scale(input_path, stdscaled.name, width=1080)
            scale(input_path, bkg.name, width=w, height=h)
            scale(input_path, bkg.name, width=1080, height=1920)
            blur(bkg.name, blur_bkg.name)
            compose_center(blur_bkg.name, stdscaled.name, output_path)
            stdscaled.close()
            bkg.close()
            blur_bkg.close()