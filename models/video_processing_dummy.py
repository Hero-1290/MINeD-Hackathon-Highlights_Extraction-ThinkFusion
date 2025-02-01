import os
import shutil
from time import sleep

def process_video(video_path):
    # Simulating the video processing delay
    print(f"Processing video: {video_path}")
    sleep(2)  # Simulate processing time

    # Simulate highlight creation (for now just copying the file)
    highlight_path = video_path.replace("uploads", "highlights").replace(".mp4", "_highlight.mp4")

    # Ensure highlights directory exists
    os.makedirs(os.path.dirname(highlight_path), exist_ok=True)

    # Simulating highlight extraction (copying the original video to highlights)
    shutil.copy(video_path, highlight_path)
    
    print(f"Video processed and saved as highlight: {highlight_path}")
    return highlight_path
