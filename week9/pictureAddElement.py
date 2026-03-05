import os
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client()

# Base image prompt: "A photorealistic picture of a fluffy ginger cat sitting on a wooden floor, looking directly at the camera. Soft, natural light from a window."
image_input = Image.open('D:\\Download\\ai-python\\week9\\big.png')
text_input = """铠甲得是金黄色的，他这个金黄色不够鲜艳，把右下角的名字去掉，这个环境换成更加恶劣的，水晶的颜色需要更亮丽点，右手手背上的光刃看起来不够锋利"""

# Generate an image from a text prompt
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[text_input, image_input],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        output_dir = "output_folder"
        os.makedirs(output_dir, exist_ok=True)
        image.save(os.path.join(output_dir, "Artanis.png"))
        print("Image saved to", os.path.join(output_dir, "Artanis.png"))