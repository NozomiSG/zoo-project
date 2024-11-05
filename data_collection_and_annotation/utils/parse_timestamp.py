# data_collection_and_annotation/utils/parse_timestamp.py

import re

def parse_timestamp(filename):
    """
    从文件名中提取时间戳（分钟和秒）
    假设文件名格式为 videoName_MM_SS.jpg
    """
    match = re.search(r"_(\d{2})_(\d{2})\.jpg$", filename)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        total_seconds = minutes * 60 + seconds
        return total_seconds
    return 0