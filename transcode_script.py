import subprocess
import os
import requests

def download_file(url, output_path):
    with open(output_path, "wb") as f:
        response = requests.get(url)
        f.write(response.content)

def transcode_video(input_file, output_dir, bitrates, resolutions, watermark_url):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Download video file
    video_path = os.path.join(output_dir, "input.mp4")
    download_file(input_file, video_path)

    # Download watermark image
    watermark_path = os.path.join(output_dir, "watermark.png")
    download_file(watermark_url, watermark_path)

    for bitrate, resolution in zip(bitrates, resolutions):
        output_path = os.path.join(output_dir, f"{resolution}_{bitrate}")
        os.makedirs(output_path, exist_ok=True)

        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", watermark_path,  # Path to the downloaded watermark image
            "-filter_complex", f"[0:v][1:v]overlay=10:10",  # Overlay watermark
            "-c:a", "copy",
            "-c:v", "libx264",
            "-b:v", f"{bitrate}k",
            "-vf", f"scale={resolution}",
            "-hls_time", "6",
            "-hls_list_size", "0",
            f"{output_path}/output.m3u8"
        ]
        subprocess.run(cmd)
        print(f"Transcoded video saved at: {output_path}")

if __name__ == "__main__":
    video_url = "https://live-par-2-abr.livepush.io/vod/bigbuckbunnyclip.mp4"  # Video URL
    output_dir = os.path.join(os.getcwd(), "output")  # Output directory in the current working directory
    bitrates = [800, 1200, 2500]  # Desired bitrates in kbps
    resolutions = ["640x360", "854x480", "1280x720"]  # Desired resolutions
    watermark_url = "https://clipart-library.com/image_gallery2/WordPress-Logo-Free-Download-PNG.png"  # Watermark URL

    transcode_video(video_url, output_dir, bitrates, resolutions, watermark_url)
