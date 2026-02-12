import time
import sys
import os
from google import genai
from google.genai import types
# 1. 导入 PIL.Image 库
from PIL import Image
# 1. 将客户端初始化移到全局范围

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Create the client
client = genai.Client(
    project="train-max-20260104",
    location="us-central1",
)

source = types.GenerateVideosSource(
    prompt="""神族和虫族在交战，飞船是折跃过来的，正对着虫族开火""",
    # 2. 修复类型错误：使用 types.Image 传递图片字节
    # The image parameter expects a types.Image object.
    image=types.Image(
        image_bytes=open("D:\\Download\\ai-python\\output_folder\\example-image-eiffel-tower2.png", "rb").read(),
        mime_type="image/png",
    )
)

config = types.GenerateVideosConfig(
    # 长宽比
    aspect_ratio="16:9",
    # 结果数量，本质是抽卡数量
    number_of_videos=1,
    # 视频时长
    duration_seconds=4,
    # 安全这块，允许（仅限成人）：默认值。仅生成成年人或成人面孔。不生成青少年或儿童的人物或面孔。
    person_generation="allow_all",
    # 是否生成音频
    generate_audio=True,
    resolution="720p",
    seed=0,
)

# Generate the video generation request
operation = client.models.generate_videos(
    model="veo-3.1-generate-001", source=source, config=config
)

# Waiting for the video(s) to be generated
while not operation.done:
    print("Video has not been generated yet. Check again in 10 seconds...")
    time.sleep(10)
    operation = client.operations.get(operation)

response = operation.result
if not response:
    print("Error occurred while generating video.")
    sys.exit(1)

generated_videos = response.generated_videos
if not generated_videos:
    print("No videos were generated.")
    sys.exit(1)

print(f"Generated {len(generated_videos)} video(s).")

for i, generated_video in enumerate(generated_videos):
    # 使用 SDK 自带的 .save() 方法保存视频
    if generated_video.video:
        output_dir = "output_folder"
        os.makedirs(output_dir, exist_ok=True)
        # 使用时间戳作为文件名
        video_filename = f"generated_video_{int(time.time())}_{i}.mp4"
        # 拼接输出路径
        output_path = os.path.join(output_dir, video_filename)
        generated_video.video.save(output_path)
        print(f"Video saved to: {output_path}")