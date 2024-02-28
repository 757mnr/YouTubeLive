#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg is not installed. Please install ffmpeg and try again."
    exit 1
fi

# Check if the input file is provided
if [ -z "$1" ]; then
    echo "Usage: $0 input.mp4"
    exit 1
fi

# Input file
input_file="$1"

# Output directory (default: same directory as input file)
output_dir=$(dirname "${input_file}")

# Output file name (without extension)
output_base=$(basename "${input_file}" .mp4)

# Output directory for HLS files
hls_dir="${output_dir}/${output_base}_hls"

# Create output directory for HLS files
mkdir -p "${hls_dir}"

# Set HLS options
hls_list_size=0 # Set to 0 to keep all segments
hls_time=10     # Set the duration of each segment (in seconds)

# Convert MP4 to HLS
ffmpeg -i "${input_file}" \
       -vf "scale=1280:-2" \
       -c:v libx264 -crf 21 -preset veryfast \
       -c:a aac \
       -hls_time "${hls_time}" \
       -hls_list_size "${hls_list_size}" \
       -hls_segment_filename "${hls_dir}/${output_base}_%03d.ts" \
       "${hls_dir}/${output_base}.m3u8"

# Check if the conversion was successful
if [ $? -eq 0 ]; then
    echo "HLS conversion completed successfully."
    echo "HLS files are saved in: ${hls_dir}/"
else
    echo "Error: HLS conversion failed."
fi
