# Step1_video_convert.py
# 该文件用于将视频转换为不同的编码格式和比特率，并解码为YUV格式

import os
import subprocess

# 文件路径
input_video = "input.mp4"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# 编码格式和比特率
codecs = ["av1_nvenc","h264_nvenc", "hevc_nvenc"]  
bitrates = [500, 1000, 1500, 2000, 2500, 3000]


def run_ffmpeg_command(cmd):
    '''运行FFmpeg命令并检查错误'''
    subprocess.run(cmd, shell=True, check=True)

def convert_video(input_file, output_file, codec, bitrate):
    '''转换视频格式并设置比特率'''
    if codec == "av1_nvenc":
        cmd = f"ffmpeg -i {input_file} -c:v {codec} -b:v {bitrate}k -preset p5 -pix_fmt yuv420p {output_file}"
    else:
        cmd = f"ffmpeg -i {input_file} -c:v {codec} -b:v {bitrate}k -pix_fmt yuv420p {output_file}"
    run_ffmpeg_command(cmd)

def decode_video(input_file, output_file):
    '''解码视频为YUV格式'''
    cmd = f"ffmpeg -i {input_file} -pix_fmt yuv420p {output_file}"
    run_ffmpeg_command(cmd)

def main():
    for codec in codecs:
        for bitrate in bitrates:
            output_file = os.path.join(output_dir, f"output_{codec}_{bitrate}k.mp4")
            convert_video(input_video, output_file, codec, bitrate)
            
            decoded_file = os.path.join(output_dir, f"output_{codec}_{bitrate}k_decoded.yuv")
            decode_video(output_file, decoded_file)

if __name__ == "__main__":
    main()