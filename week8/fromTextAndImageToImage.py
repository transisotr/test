from google import genai
from PIL import Image
import os

client = genai.Client()

prompt = (
    "请根据我的证件照生成二次元风格的头像，要求保持阳光和积极向上的样子",
)

image = Image.open("D:\\Download\\ai-python\\week8\\person.jpg")

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt, image],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        output_dir = "output_folder"
        os.makedirs(output_dir, exist_ok=True)
        image.save(os.path.join(output_dir, "cartoon.png"))
        print("Image saved to", os.path.join(output_dir, "cartoon.png"))

