# Step3_plot.py
# 该文件用于绘制不同编码格式和比特率下的质量指标（PSNR、SSIM、LPIPS）对比图

import matplotlib.pyplot as plt
import pandas as pd
import os
import re

def main():
    script_dir = os.path.dirname(__file__)
    csv_file = os.path.join(script_dir, "output", "quality_metrics.csv")  # 确保路径正确

    data = pd.read_csv(csv_file)

    required_columns = ['File', 'Average PSNR', 'Average SSIM', 'Average LPIPS']  # 确保 CSV 文件包含这些列
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"CSV file is missing required column: {col}")

    def extract_codec_and_bitrate(filename):
        match = re.search(r'output_(\w+)_(\d+)k_', filename)  # 正则表达式匹配 codec 和 bitrate
        if match:
            return match.group(1), int(match.group(2))
        else:
            return None, None

    data[['Codec', 'bitrate']] = data['File'].apply(
        lambda x: pd.Series(extract_codec_and_bitrate(x))
    )

    if data['Codec'].isnull().any() or data['bitrate'].isnull().any():
        raise ValueError("Failed to extract codec or bitrate from some filenames. Please check the filename format.")

    codecs = data['Codec'].unique()

    # 绘制图形
    plt.figure(figsize=(15, 5))

    # PSNR 子图
    plt.subplot(1, 3, 1)
    for codec in codecs:
        codec_data = data[data['Codec'] == codec].sort_values(by='bitrate')  # 按码率排序
        plt.plot(codec_data['bitrate'], codec_data['Average PSNR'], marker='o', linestyle='-', label=f'{codec}')
    plt.xlabel('Bitrate (kbps)')
    plt.ylabel('Average PSNR')
    plt.title('Bitrate vs PSNR')
    plt.legend()
    plt.grid(True)

    # SSIM 子图
    plt.subplot(1, 3, 2)
    for codec in codecs:
        codec_data = data[data['Codec'] == codec].sort_values(by='bitrate')  # 按码率排序
        plt.plot(codec_data['bitrate'], codec_data['Average SSIM'], marker='o', linestyle='-', label=f'{codec}')
    plt.xlabel('Bitrate (kbps)')
    plt.ylabel('Average SSIM')
    plt.title('Bitrate vs SSIM')
    plt.legend()
    plt.grid(True)

    # LPIPS 子图
    plt.subplot(1, 3, 3)
    for codec in codecs:
        codec_data = data[data['Codec'] == codec].sort_values(by='bitrate')  # 按码率排序
        plt.plot(codec_data['bitrate'], codec_data['Average LPIPS'], marker='o', linestyle='-', label=f'{codec}')
    plt.xlabel('Bitrate (kbps)')
    plt.ylabel('Average LPIPS')
    plt.title('Bitrate vs LPIPS')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join("output", "bitrate_vs_quality_metrics_combined.png"))
    plt.show()

if __name__ == "__main__":
    main()