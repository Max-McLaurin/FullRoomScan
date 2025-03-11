# video_processor.py
import cv2
import os
from config import OUTPUT_DIR

def extract_frames(video_path, output_folder=OUTPUT_DIR, interval_seconds=2):
    """
    Extracts frames from a video at a set time interval.
    
    Args:
    - video_path (str): Path to the input video.
    - output_folder (str): Directory to save extracted frames.
    - interval_seconds (int): Extract one frame every N seconds.
    
    Returns:
    - List[str]: Paths of extracted frames.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get frames per second
    if fps == 0 or fps is None:
        print("Error: Unable to retrieve FPS from video.")
        return []

    frame_interval = int(fps * interval_seconds)  # Convert seconds to frame count
    frame_count = 0
    success, image = cap.read()
    saved_frames = []

    while success:
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_filename, image)
            saved_frames.append(frame_filename)

        success, image = cap.read()
        frame_count += 1

    cap.release()
    print(f"Extracted {len(saved_frames)} frames from video.")
    return saved_frames

if __name__ == "__main__":
    # Test with a sample video
    extracted_frames = extract_frames("sample_video.MOV", "./output", interval_seconds=2)
    print("Extracted frames:", extracted_frames)
