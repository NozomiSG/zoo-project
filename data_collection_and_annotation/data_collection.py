# data_collection_and_annotation/data_collection.py

import os
from frame_extraction import extract_frames
from annotation_processing import process_frames

def main(video_path, output_folder, tmp_frame_folder):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_output_folder = os.path.join(output_folder, video_name)
    os.makedirs(video_output_folder, exist_ok=True)

    # 提取视频帧
    extract_frames(video_path, tmp_frame_folder)

    # 处理提取的帧
    process_frames(tmp_frame_folder, video_name, video_output_folder)

    # 删除临时帧文件夹
    # 如果不想保留临时帧，可以取消注释以下行
    # shutil.rmtree(tmp_frame_folder)

if __name__ == "__main__":
    # 配置路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

    tmp_frame_folder = os.path.join(current_dir, "tmp_frames")
    output_folder = os.path.join(current_dir, "../data/annotations")

    video_folder = os.path.join(current_dir, "../data/raw_videos")

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(tmp_frame_folder, exist_ok=True)

    # 处理视频文件夹中的所有视频
    video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".avi", ".mov"))]
    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        print(f"Processing video: {video_path}")
        main(video_path, output_folder, tmp_frame_folder)
        print(f"Finished processing video: {video_path}")
        print("------------------------")

    # 清理临时帧文件夹
    # 如果希望在所有视频处理完后删除临时帧文件夹，可以取消注释以下行
    # shutil.rmtree(tmp_frame_folder)