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

    # Download watermark image
    watermark_path = os.path.join(output_dir, "watermark.png")
    download_file(watermark_url, watermark_path)

    for bitrate, resolution in zip(bitrates, resolutions):
        output_path = os.path.join(output_dir, f"{resolution}_{bitrate}.m3u8")
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-i", watermark_path,  # Path to the downloaded watermark image
            "-filter_complex", f"[0:v][1:v]overlay=10:10",  # Overlay watermark
            "-c:a", "copy",
            "-c:v", "libx264",
            "-b:v", f"{bitrate}k",
            "-vf", f"scale={resolution}",
            "-hls_time", "6",
            "-hls_list_size", "0",
            output_path
        ]
        subprocess.run(cmd)

if __name__ == "__main__":
    input_file = "https://live-par-2-abr.livepush.io/vod/bigbuckbunnyclip.mp4"  # Video URL
    output_dir = "output"      # Output directory
    bitrates = [800, 1200, 2500]  # Desired bitrates in kbps
    resolutions = ["640x360", "854x480", "1280x720"]  # Desired resolutions
    watermark_url = "https://clipart-library.com/image_gallery2/WordPress-Logo-Free-Download-PNG.png"  # Watermark URL

    transcode_video(input_file, output_dir, bitrates, resolutions, watermark_url)
