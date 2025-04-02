# Step0_environment_check.py
# 文件用于检查环境配置是否正确，包括PyTorch、CUDA、pyiqa、matplotlib、pandas和FFmpeg的安装情况。
# 如果缺少任何库或工具，将提示用户安装相应的库或工具，并给出安装命令或链接。
# 该文件在运行其他脚本之前执行，以确保环境配置正确。

import torch
import subprocess

# 检查PyTorch和CUDA安装情况
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("CUDA device count:", torch.cuda.device_count())
    print("CUDA device name:", torch.cuda.get_device_name(0))
else:
    print("CUDA is not available. Please check if the CUDA driver and GPU are installed correctly.")

# 检查pyiqa安装情况
try:
    import pyiqa
    print("Pyiqa version:", pyiqa.__version__)
except ImportError:
    print("Pyiqa is not installed. Please install it using the following command:")
    print("pip install pyiqa")

# 检查matplotlib和pandas安装情况
try:
    import matplotlib
    import pandas
    print("Matplotlib version:", matplotlib.__version__)
    print("Pandas version:", pandas.__version__)
except ImportError as e:
    missing_package = str(e).split("'")[1]
    print(f"{missing_package} is not installed. Please install it using the following command:")
    print(f"pip install {missing_package}")

# 检查FFmpeg编码器支持情况
try:
    output = subprocess.check_output("ffmpeg -encoders", shell=True).decode()
    if "h264_nvenc" in output and "hevc_nvenc" in output and "av1_nvenc" in output:
        print("GPU encoder support is normal: h264_nvenc, hevc_nvenc, av1_nvenc")
    else:
        print("GPU encoder support is incomplete. Please check the NVIDIA driver and FFmpeg build configuration.")
except subprocess.CalledProcessError:
    print("Unable to validate FFmpeg encoder support. Please check if FFmpeg is installed correctly.")
    

# 检查FFmpeg安装情况
try:
    print("FFmpeg version:", subprocess.check_output("ffmpeg -version", shell=True).decode())
except FileNotFoundError:
    print("FFmpeg is not installed. Please ensure FFmpeg is installed and added to the PATH.")
    print("Linux: sudo apt install ffmpeg")
    print("Windows: Download from https://ffmpeg.org and configure the PATH")    