# data_collection_and_annotation/frame_extraction.py

import cv2
import os

def extract_frames(video_path, output_folder):
    """
    提取视频帧，统一使用10秒间隔
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps  # 视频总时长(秒)

    frame_count = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        current_time = frame_count / fps

        # 每10秒保存一帧
        if current_time % 10 < 1 / fps:
            minutes = int(current_time // 60)
            seconds = int(current_time % 60)
            output_path = os.path.join(
                output_folder,
                f"{os.path.splitext(os.path.basename(video_path))[0]}_{minutes:02d}_{seconds:02d}.jpg"
            )
            cv2.imwrite(output_path, frame)

        frame_count += 1

    video.release()
    print(f"视频时长: {duration:.2f}秒")
    print(f"已提取帧保存至: {output_folder}")