# data_collection_and_annotation/object_detection.py

import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

# 初始化模型和处理器
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Florence-2-large",
    torch_dtype=torch_dtype,
    trust_remote_code=True
).to(device)

processor = AutoProcessor.from_pretrained("microsoft/Florence-2-large", trust_remote_code=True)

# 定义提示符和标签列表
OD_PROMPT = "<OD>"
CAPTION_PROMPT = "<CAPTION>"
LABEL_COLLECTED = []
ANIMAL_LABELS = ['lion', 'tiger', 'elephant', 'animal', 'carnivore']

def llm_generate(image, task_prompt, text_input=None):
    if text_input is None:
        prompt = task_prompt
    else:
        prompt = task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)
    generated_ids = model.generate(
        input_ids=inputs["input_ids"].to(device),
        pixel_values=inputs["pixel_values"].to(device),
        max_new_tokens=1024,
        early_stopping=False,
        do_sample=False,
        num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(
        generated_text,
        task=task_prompt,
        image_size=image.size
    )

    return parsed_answer