# data_collection_and_annotation/annotation_processing.py

import os
import pandas as pd
import shutil
import time
from PIL import Image

from object_detection import llm_generate, OD_PROMPT, CAPTION_PROMPT, LABEL_COLLECTED, ANIMAL_LABELS
from utils.draw_bboxes import draw_bboxes
from utils.parse_timestamp import parse_timestamp

def process_frames(frame_folder, video_name, output_folder):
    """
    处理提取的帧，进行对象检测和描述
    """
    results = []
    type_count = {}
    count = 0
    frame_files = sorted(
        [f for f in os.listdir(frame_folder) if f.endswith(".jpg")],
        key=lambda x: parse_timestamp(x)
    )

    in_animal_detection = False
    next_detection_time = 0

    for frame_file in frame_files:
        frame_path = os.path.join(frame_folder, frame_file)
        timestamp = parse_timestamp(frame_file)

        # 如果不在动物检测期间，只处理每60秒的帧
        if not in_animal_detection and timestamp % 60 != 0:
            continue

        # 如果在动物检测期间，处理每10秒的帧
        if in_animal_detection and timestamp < next_detection_time:
            continue

        image = Image.open(frame_path).convert("RGB")
        od_result = llm_generate(image, OD_PROMPT)
        detected_labels = od_result.get('<OD>').get('labels', [])
        detected_bboxes = od_result.get('<OD>').get('bboxes', [])

        for label in detected_labels:
            type_count[label.lower()] = type_count.get(label.lower(), 0) + 1
        for label in detected_labels:
            if label.lower() not in LABEL_COLLECTED:
                LABEL_COLLECTED.append(label.lower())
        animals_detected = [label for label in detected_labels if label.lower() in ANIMAL_LABELS]
        animal_indices = [i for i, label in enumerate(detected_labels) if label.lower() in ANIMAL_LABELS]
        animal_bboxes = [detected_bboxes[i] for i in animal_indices]
        animal_labels = [detected_labels[i] for i in animal_indices]

        if animals_detected:
            count += 1
            print(f"[{timestamp}s] 检测到动物: {animals_detected} - {frame_file}")
            caption = llm_generate(image, CAPTION_PROMPT)
            caption = caption['<CAPTION>']
            result = {
                'Time (s)': timestamp,
                'Labels': ', '.join(detected_labels),
                'BBoxes': detected_bboxes,
                'Caption': caption
            }
            results.append(result)
            in_animal_detection = True
            next_detection_time = timestamp + 10

            # 如果是60秒间隔的帧，保存带边界框的图像
            if timestamp % 60 == 0:
                marked_image = draw_bboxes(frame_path, animal_bboxes, animal_labels)
                output_image_path = os.path.join(
                    output_folder,
                    f"detected_{os.path.basename(frame_file)}"
                )
                marked_image.save(output_image_path)
                print(f"[{timestamp}s] 已保存带边界框的图像: {output_image_path}")
        else:
            print(f"[{timestamp}s] 未检测到动物。")
            if in_animal_detection:
                print(f"[{timestamp}s] 动物已消失。停止进一步检测。")
                in_animal_detection = False

    print("动物类型统计:", type_count)
    print("总共检测到动物的次数:", count)

    if results:
        df = pd.DataFrame(results)
        output_file_csv = os.path.join(output_folder, f"{video_name}.csv")
        output_file_excel = os.path.join(output_folder, f"{video_name}.xlsx")
        df.to_csv(output_file_csv, index=False)
        df.to_excel(output_file_excel, index=False)
        print(f"结果已保存到 {output_file_csv} 和 {output_file_excel}")
    else:
        print("未检测到任何动物。")

    # 清理临时帧文件夹
    clean_tmp_frames(frame_folder)

def clean_tmp_frames(folder):
    """
    清理临时帧文件夹
    """
    try:
        shutil.rmtree(folder)
        print(f"已清理临时文件夹: {folder}")
    except Exception as e:
        print(f"清理临时文件夹时出错: {e}")