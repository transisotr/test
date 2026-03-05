from pathlib import Path
import time

from google import genai
from google.genai import types
import yt_dlp

VIDEO_URL = "https://www.bilibili.com/video/BV1LVqHByEGE"
OUTPUT_DIR = Path(r"D:\Download\ai-python\output_folder")
TEMP_VIDEO_PATH = OUTPUT_DIR / "temp_bilibili_video.mp4"

client = genai.Client()

# 使用 Python 库 yt-dlp 下载bilibili视频
# pip install yt-dlp
# 安装 ffmpeg
# pip install ffmpeg
def download_video(url, output_path):
    """使用 yt-dlp 下载并合并音视频"""
    print(f"正在下载视频: {url}")
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': str(output_path),
        'quiet': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"下载完成: {output_path}")

def upload_video(video_path):
    """上传视频并调用 Gemini 转录"""
    # 上传文件
    print("正在上传文件到 Google...")
    video_file = client.files.upload(
        file=video_path
    )
    
    # 等待处理完成
    print(f"上传成功，等待服务端处理 (ID: {video_file.name})...")
    while video_file.state.name == "PROCESSING":
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)
    
    if video_file.state.name == "FAILED":
        raise ValueError("视频处理失败")
    
    print("视频处理就绪，开始转录...")

    return video_file

def gemini_transcribe(audio_file):
  prompt = """
    请根据视频内容生成详细的逐字稿。
    要求：
    1. 提供每个段落的时间戳 (格式: MM:SS)。
    2. 检测每个段落的主要语言，如果是外语请提供中文翻译。
    3. 识别讲话者的情感 (Happy, Sad, Angry, Neutral)。
    4. 开头先提供一段简短的内容总结。
    """

  response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
      types.Content(
        parts=[
          types.Part(
            file_data=types.FileData(
              file_uri=audio_file.uri,
              mime_type=audio_file.mime_type
            )
          ),
          types.Part(
            text=prompt
          )
        ]
      )
    ],
    config=types.GenerateContentConfig(
      response_mime_type="application/json",
    #   response_mime_type="application/text",
      response_schema=types.Schema(
        type=types.Type.OBJECT,
        properties={
          "summary": types.Schema(
            type=types.Type.STRING,
            description="A concise summary of the audio content.",
          ),
          "segments": types.Schema(
            type=types.Type.ARRAY,
            description="List of transcribed segments with timestamp.",
            items=types.Schema(
              type=types.Type.OBJECT,
              properties={
                # json 输出格式
                "timestamp": types.Schema(type=types.Type.STRING),
                "content": types.Schema(type=types.Type.STRING),
                "language": types.Schema(type=types.Type.STRING),
                "language_code": types.Schema(type=types.Type.STRING),
                "translation": types.Schema(type=types.Type.STRING),
                "emotion": types.Schema(
                  type=types.Type.STRING,
                  enum=["happy", "sad", "angry", "neutral"]
                ),
              },
              required=["timestamp", "content", "language", "language_code", "emotion"],
            ),
          ),
        },
        required=["summary", "segments"],
      ),
    ),
  )

  return response

def main():
  
#   download_video(VIDEO_URL, TEMP_VIDEO_PATH)

  video_file = upload_video(TEMP_VIDEO_PATH)

  response = gemini_transcribe(video_file)

#   # 3. 拼接路径并写入
  file_path = OUTPUT_DIR / "output.txt"
  with open(file_path, "w", encoding="utf-8") as f:
      f.write(response.text)
  print(response.text)

if __name__ == "__main__":
  main()
