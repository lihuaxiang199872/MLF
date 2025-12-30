import yt_dlp
import subprocess
import os


def download_bilibili_simple(url, output_dir="videos"):
    """
    最简单的下载方案，让yt-dlp自动处理一切
    """
    # 创建目录
    os.makedirs(output_dir, exist_ok=True)

    # 使用命令行方式，更稳定
    cmd = [
        'yt-dlp',
        '-o', f'{output_dir}/%(title)s.%(ext)s',
        '--no-warnings',
        '--ignore-errors',
        '--retries', '10',
        '--fragment-retries', '10',
        '--buffer-size', '16K',
        '--http-chunk-size', '10M',
        '--concurrent-fragments', '5',
        '--throttled-rate', '100K',
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '--referer', 'https://www.bilibili.com',
        url
    ]

    print("执行命令:", ' '.join(cmd))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ 下载成功!")
            print("输出:", result.stdout)

            # 查找下载的文件
            for line in result.stdout.split('\n'):
                if 'Destination:' in line:
                    file_path = line.split('Destination:')[1].strip()
                    if os.path.exists(file_path):
                        print(f"文件位置: {file_path}")
                        return file_path
        else:
            print("✗ 下载失败!")
            print("错误信息:", result.stderr)

    except FileNotFoundError:
        print("错误: 请先安装 yt-dlp")
        print("安装命令: pip install yt-dlp")
    except Exception as e:
        print(f"未知错误: {e}")

    return None


def get_simple_link(url):
    """
    获取最简单直接的下载链接
    """
    try:
        # 使用yt-dlp获取信息
        cmd = ['yt-dlp', '-g', '--no-warnings', url]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            links = result.stdout.strip().split('\n')
            print(f"找到 {len(links)} 个链接:")
            for i, link in enumerate(links, 1):
                print(f"{i}. {link[:80]}...")
            return links
        else:
            print("获取链接失败:", result.stderr)
            return []

    except Exception as e:
        print(f"错误: {e}")
        return []


# 使用
if __name__ == "__main__":
    # 替换成你的视频URL
    video_url = "https://www.bilibili.com/video/BV1QwbWzgEKJ"

    print("方案1: 自动下载")
    download_bilibili_simple(video_url,'BV1QwbWzgEKJ')
