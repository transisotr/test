import os
from io import BytesIO
from google import genai
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image

# 调用模型生成图片

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

client = genai.Client(
    project="train-max-20260104",  
    location="global"
)

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=("生成星际争霸2的亚顿之矛，背景是艾尔"),
    config=GenerateContentConfig(
        response_modalities=[Modality.TEXT, Modality.IMAGE],
    ),
)
for part in response.candidates[0].content.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = Image.open(BytesIO((part.inline_data.data)))
        # Ensure the output directory exists
        output_dir = "output_folder"
        os.makedirs(output_dir, exist_ok=True)
        image.save(os.path.join(output_dir, "example-image-eiffel-tower.png"))


