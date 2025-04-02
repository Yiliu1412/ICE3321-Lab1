# Step2_frame_extract_and_stitch.py
# 该文件用于从视频中提取特定帧，并进行横向拼接
import os
import subprocess
from PIL import Image

# 文件路径
input_video = "input.mp4"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 提取帧的时间点
frame_time = "00:00:07"

def run_ffmpeg_command(cmd):
    '''运行FFmpeg命令并检查错误'''
    subprocess.run(cmd, shell=True, check=True)

def extract_frame(input_file, output_file, time):
    '''从视频中提取特定帧'''
    cmd = f"ffmpeg -i {input_file} -ss {time} -vframes 1 {output_file}"
    run_ffmpeg_command(cmd)

def stitch_images_horizontally(image_files, output_file):
    '''将多张图片横向拼接'''
    images = [Image.open(img) for img in image_files]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_image = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.size[0]
    new_image.save(output_file)

def main():
    # 提取原视频的帧
    frame_original = os.path.join(output_dir, "frame_original.png")
    extract_frame(input_video, frame_original, frame_time)

    # 第一张横图：原视频 + h264 500k + hevc 500k + av1 500k
    frame_h264_500k = os.path.join(output_dir, "frame_h264_nvenc_500k.png")
    frame_hevc_500k = os.path.join(output_dir, "frame_hevc_nvenc_500k.png")
    frame_av1_500k = os.path.join(output_dir, "frame_av1_nvenc_500k.png")
    extract_frame(os.path.join(output_dir, "output_h264_nvenc_500k.mp4"), frame_h264_500k, frame_time)
    extract_frame(os.path.join(output_dir, "output_hevc_nvenc_500k.mp4"), frame_hevc_500k, frame_time)
    extract_frame(os.path.join(output_dir, "output_av1_nvenc_500k.mp4"), frame_av1_500k, frame_time)
    
    stitched_original_500k = os.path.join(output_dir, "stitched_original_h264_500k_hevc_500k_av1_500k.png")
    stitch_images_horizontally([frame_original, frame_h264_500k, frame_hevc_500k, frame_av1_500k], stitched_original_500k)

    # 第二张横图：h264 1000k + h264 2000k + h264 3000k
    frame_h264_1000k = os.path.join(output_dir, "frame_h264_nvenc_1000k.png")
    frame_h264_2000k = os.path.join(output_dir, "frame_h264_nvenc_2000k.png")
    frame_h264_3000k = os.path.join(output_dir, "frame_h264_nvenc_3000k.png")
    extract_frame(os.path.join(output_dir, "output_h264_nvenc_1000k.mp4"), frame_h264_1000k, frame_time)
    extract_frame(os.path.join(output_dir, "output_h264_nvenc_2000k.mp4"), frame_h264_2000k, frame_time)
    extract_frame(os.path.join(output_dir, "output_h264_nvenc_3000k.mp4"), frame_h264_3000k, frame_time)
    
    stitched_h264_1000k_2000k_3000k = os.path.join(output_dir, "stitched_h264_1000k_h264_2000k_h264_3000k.png")
    stitch_images_horizontally([frame_h264_1000k, frame_h264_2000k, frame_h264_3000k], stitched_h264_1000k_2000k_3000k)

    # 第三张横图：hevc 1000k + hevc 2000k + hevc 3000k
    frame_hevc_1000k = os.path.join(output_dir, "frame_hevc_nvenc_1000k.png")
    frame_hevc_2000k = os.path.join(output_dir, "frame_hevc_nvenc_2000k.png")
    frame_hevc_3000k = os.path.join(output_dir, "frame_hevc_nvenc_3000k.png")
    extract_frame(os.path.join(output_dir, "output_hevc_nvenc_1000k.mp4"), frame_hevc_1000k, frame_time)
    extract_frame(os.path.join(output_dir, "output_hevc_nvenc_2000k.mp4"), frame_hevc_2000k, frame_time)
    extract_frame(os.path.join(output_dir, "output_hevc_nvenc_3000k.mp4"), frame_hevc_3000k, frame_time)
    
    stitched_hevc_1000k_2000k_3000k = os.path.join(output_dir, "stitched_hevc_1000k_hevc_2000k_hevc_3000k.png")
    stitch_images_horizontally([frame_hevc_1000k, frame_hevc_2000k, frame_hevc_3000k], stitched_hevc_1000k_2000k_3000k)

    # 第四张横图：av1 1000k + av1 2000k + av1 3000k
    frame_av1_1000k = os.path.join(output_dir, "frame_av1_nvenc_1000k.png")
    frame_av1_2000k = os.path.join(output_dir, "frame_av1_nvenc_2000k.png")
    frame_av1_3000k = os.path.join(output_dir, "frame_av1_nvenc_3000k.png")
    extract_frame(os.path.join(output_dir, "output_av1_nvenc_1000k.mp4"), frame_av1_1000k, frame_time)
    extract_frame(os.path.join(output_dir, "output_av1_nvenc_2000k.mp4"), frame_av1_2000k, frame_time)
    extract_frame(os.path.join(output_dir, "output_av1_nvenc_3000k.mp4"), frame_av1_3000k, frame_time)
    
    stitched_av1_1000k_2000k_3000k = os.path.join(output_dir, "stitched_av1_1000k_av1_2000k_av1_3000k.png")
    stitch_images_horizontally([frame_av1_1000k, frame_av1_2000k, frame_av1_3000k], stitched_av1_1000k_2000k_3000k)

if __name__ == "__main__":
    main()