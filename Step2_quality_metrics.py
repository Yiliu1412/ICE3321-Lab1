# Step2_quality_metrics.py
# 该文件用于计算解码后YUV文件的质量指标（PSNR、SSIM、LPIPS），并将结果保存到CSV文件中

import os
import csv
import torch
from pyiqa.archs.psnr_arch import psnr
from pyiqa.archs.ssim_arch import ssim
from pyiqa.archs.lpips_arch import LPIPS 
import numpy as np

# 文件路径和参数
input_yuv = "input.yuv"
output_dir = "output"
width = 1080
height = 1920
output_csv = os.path.join(output_dir, "quality_metrics.csv")  # 确保路径正确，step3将会读取这个文件

def read_yuv_file(file_path, width, height):
    '''读取YUV文件并返回帧数据'''
    frame_size = width * height * 3 // 2
    with open(file_path, "rb") as f:
        yuv_data = f.read()
    return np.frombuffer(yuv_data, dtype=np.uint8).reshape(-1, frame_size)

def compare_quality(ref_yuv, target_yuv, width, height):
    ''''比较参考YUV和目标YUV的质量指标（PSNR、SSIM、LPIPS）'''
    if ref_yuv.shape != target_yuv.shape:
        raise ValueError(f"YUV frame count or resolution mismatch: ref={ref_yuv.shape}, target={target_yuv.shape}")
    
    psnr_values = []
    ssim_values = []
    lpips_values = []  
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")   # 使用GPU加速
    lpips_model = LPIPS(net='alex').to(device)  # 初始化 LPIPS 模型

    for ref_frame, target_frame in zip(ref_yuv, target_yuv):
        ref_frame = ref_frame.reshape(height * 3 // 2, width)
        target_frame = target_frame.reshape(height * 3 // 2, width)
        
        ref_y = ref_frame[:height, :].copy()
        target_y = target_frame[:height, :].copy()
        
        ref_y_tensor = torch.from_numpy(ref_y).float().unsqueeze(0).unsqueeze(0).to(device) / 255.0
        target_y_tensor = torch.from_numpy(target_y).float().unsqueeze(0).unsqueeze(0).to(device) / 255.0
        
        psnr_value = psnr(ref_y_tensor, target_y_tensor, data_range=1.0).item()
        psnr_values.append(psnr_value)
        
        ssim_value = ssim(ref_y_tensor, target_y_tensor, data_range=1.0).item()
        ssim_values.append(ssim_value)
        
        lpips_value = lpips_model(ref_y_tensor, target_y_tensor).item()  
        lpips_values.append(lpips_value)
    
    return np.mean(psnr_values), np.mean(ssim_values), np.mean(lpips_values)  

def main():
    print(f"Reading original YUV file: {input_yuv}")
    ref_yuv = read_yuv_file(input_yuv, width, height)
    
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File", "Average PSNR", "Average SSIM", "Average LPIPS"])  
        
        for file_name in os.listdir(output_dir):
            if file_name.endswith("_decoded.yuv"):
                target_yuv_path = os.path.join(output_dir, file_name)
                print(f"Comparing file: {target_yuv_path}")
                
                target_yuv = read_yuv_file(target_yuv_path, width, height)
                
                try:
                    avg_psnr, avg_ssim, avg_lpips = compare_quality(ref_yuv, target_yuv, width, height)  # 获取 LPIPS
                    print(f"File: {file_name}")
                    print(f"Average PSNR: {avg_psnr:.4f}")
                    print(f"Average SSIM: {avg_ssim:.4f}")
                    print(f"Average LPIPS: {avg_lpips:.4f}")  
                    print("-" * 40)
                    
                    writer.writerow([file_name, f"{avg_psnr:.4f}", f"{avg_ssim:.4f}", f"{avg_lpips:.4f}"])  # 写入 LPIPS
                except ValueError as e:
                    print(f"Skipping file {file_name}: {e}")
    
    print(f"Quality metrics saved to: {output_csv}")

if __name__ == "__main__":
    main()