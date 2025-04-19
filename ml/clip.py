import subprocess

def cut(input_path, output_path, start_time, end_time):
    cmd = [
        'ffmpeg',
        '-ss', str(start_time),
        '-to', str(end_time),
        '-i', input_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'fast',    
        output_path
    ]

    subprocess.run(cmd)

def scale(path, output, width=900, height=1600):
    subprocess.run(["ffmpeg", "-i", path, "-vf",
                    f"scale={width}:{height}", output])

def border(input_path, output_path, border_hd=0, border_lr=0, border_color="black"):
    """
    Add border using FFmpeg (faster for large videos)
    :param border_color: Can be color name or hex code (#RRGGBB)
    :param border_hd: size of border under and upper of original video (total height increased on border_hd*2)
    :param border_lr: size of left and right border (total width increased on border_lr*2l)
    """
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'pad=width=iw+{border_lr*2}:height=ih+{border_hd*2}:x={border_lr}:y={border_hd}:color={border_color}',
        '-c:a', 'copy',
        output_path
    ]

    subprocess.run(cmd)

def blur(input_path, output_path):
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', 'boxblur=10:5',
        '-c:a', 'copy',
        output_path
    ]

    subprocess.run(cmd)

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