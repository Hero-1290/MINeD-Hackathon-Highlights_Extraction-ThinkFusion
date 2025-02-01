import cv2
import ffmpeg
import numpy as np
import os

FFMPEG_PATH = "C:/Users/Bhaumit/Important Software Files/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe"


def detect_gunshots_kills(video_path):
    """Detect timestamps of gunfire, kills, and explosions, ensuring full action sequences are captured."""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    print(f"Video Duration: {duration:.2f} seconds")

    gunfire_timestamps = []
    kill_events = []
    death_events = []
    previous_brightness = 0

    frame_index = 0
    last_gunshot_time = -10  # Track last gunshot

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gunfire Detection - Measure brightness change
        brightness = np.mean(gray)
        if brightness - previous_brightness > 50:  # Gunfire flash detection
            gunfire_timestamps.append(frame_index / fps)
            last_gunshot_time = frame_index / fps  # Update last gunfire time

        previous_brightness = brightness

        # Detect "Kill Event" (Text Detection)
        roi = gray[50:100, 100:500]  # Assume kill message appears at top-left
        _, thresh = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)
        white_pixels = np.sum(thresh == 255)

        if white_pixels > 5000:  # Arbitrary threshold for detecting kill messages
            kill_events.append(frame_index / fps)

        # Detect "Death Event" (Screen Goes Dark or Death Text Appears)
        if brightness < 30:  # Dark screen = Possible death
            death_events.append(frame_index / fps)

        frame_index += 1

    cap.release()

    # Merge close events (If events happen within 3 sec, merge them)
    highlight_ranges = []
    all_events = sorted(set(gunfire_timestamps + kill_events + death_events))

    if all_events:
        start_time = max(0, all_events[0] - 5)  # Start 5 sec before first action
        for i in range(1, len(all_events)):
            if all_events[i] - all_events[i - 1] > 3:
                highlight_ranges.append((start_time, all_events[i - 1] + 3))
                start_time = max(0, all_events[i] - 5)  # Capture action leading to kill
        highlight_ranges.append((start_time, all_events[-1] + 3))

    return highlight_ranges


def create_highlight_video(input_video, output_video, highlight_ranges):
    """Trim only kill/gunfire moments, include audio, and merge them smoothly."""
    output_dir = os.path.dirname(output_video)
    os.makedirs(output_dir, exist_ok=True)

    input_files = []
    for i, (start_time, end_time) in enumerate(highlight_ranges):
        duration = end_time - start_time
        temp_output = f"temp_highlight_{i + 1}.mp4"

        ffmpeg.input(input_video, ss=start_time, t=duration).output(
            temp_output, vcodec="libx264", acodec="aac", audio_bitrate="192k"
        ).run(cmd=FFMPEG_PATH)

        input_files.append(temp_output)

    # Merge all highlights into one final video
    with open("input_list.txt", "w") as f:
        for temp_file in input_files:
            f.write(f"file '{temp_file}'\n")

    ffmpeg.input("input_list.txt", format="concat", safe=0).output(
        output_video, vcodec="libx264", acodec="aac", audio_bitrate="192k"
    ).run(cmd=FFMPEG_PATH)

    print(f"Final highlight video created: {output_video}")

    # Cleanup temp files
    for temp_file in input_files:
        os.remove(temp_file)
    os.remove("input_list.txt")


def main():
    video_file = "F:/game-highlights-extraction/uploads/new_v.mp4"
    highlight_output_video = "highlights/final_highlight_video.mp4"

    if not os.path.exists(video_file):
        print("Error: Video file not found.")
        return

    highlight_ranges = detect_gunshots_kills(video_file)
    create_highlight_video(video_file, highlight_output_video, highlight_ranges)


if __name__ == "__main__":
    main()
