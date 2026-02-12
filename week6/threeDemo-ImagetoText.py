import os
from google import genai
from google.genai.types import HttpOptions
from PIL import Image

# 根据图片生成描述信息

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# 1. 客户端初始化需要 project 和 location，与 onedemo.py 保持一致。
# 2. 使用 v1beta1 API 版本以获得更好的兼容性。
client = genai.Client(
    project="train-max-20260104",
    location="global",
    http_options=HttpOptions(api_version="v1")
)

# 3. 使用 PIL.Image 打开本地图片，而不是 Part.from_uri。
img = Image.open("D:\\Download\\ai-python\\output_folder\\example-image-eiffel-tower.png")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["这张图里画的是什么？", img],
)
print(response.text)

