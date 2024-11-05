# data_collection_and_annotation/utils/draw_bboxes.py

from PIL import Image, ImageDraw, ImageFont
import random
import os

def draw_bboxes(image_path, bboxes, labels):
    """
    在图像上绘制边界框和标签
    """
    # 读取图像
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # 为不同标签设置不同颜色
    unique_labels = list(set(labels))
    colors = {}
    for label in unique_labels:
        colors[label] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 加载字体
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.exists(font_path):
        font_path = None  # 使用默认字体
    font_size = 16
    font = ImageFont.truetype(font_path, font_size) if font_path else None

    for bbox, label in zip(bboxes, labels):
        # 获取坐标
        x1, y1, x2, y2 = bbox

        # 确保坐标在图像范围内
        x1 = max(0, min(x1, width))
        y1 = max(0, min(y1, height))
        x2 = max(0, min(x2, width))
        y2 = max(0, min(y2, height))

        # 获取当前标签的颜色
        color = colors[label]

        # 绘制边界框
        draw.rectangle([x1, y1, x2, y2], outline=color, width=2)

        # 添加标签文本背景
        text = label
        text_size = draw.textsize(text, font=font)
        text_background = [x1, y1 - text_size[1], x1 + text_size[0], y1]
        draw.rectangle(text_background, fill=color)

        # 绘制标签文本
        draw.text((x1, y1 - text_size[1]), text, fill=(255, 255, 255), font=font)

    return image