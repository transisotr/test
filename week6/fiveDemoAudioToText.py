from google import genai
from google.genai import types
import base64
import os
from google.genai.types import HttpOptions

# 根据音频生成文本，对音频内容进行分析和总结

def generate():
  os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
#   client = genai.Client(
#       vertexai=True,
#       api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
#       api_key = os.environ.get("GEMINI_API_KEY")
#   )
  client = genai.Client(
    project="train-max-20260104",  
    location="global",             
    http_options=HttpOptions(api_version="v1")
)

  audio1 = types.Part.from_uri(
      file_uri="gs://cloud-samples-data/generative-ai/audio/Accessible_writing_tip_Informative_semantic_titles_and_headings.mp3",
      mime_type="audio/mpeg",
  )
# 模型可选择
  model = "gemini-2.5-flash"

# 提示词和源文件
  contents = [
    types.Content(
      role="user",
      parts=[
        types.Part.from_text(text="""Please analyze this audio file and summarize the contents of the audio as bullet points."""),
        audio1
      ]
    )
  ]

# 安全方面的配置
  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 1,
    max_output_tokens = 65535,
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    thinking_config=types.ThinkingConfig(
      thinking_budget=-1,
    ),
  )

  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    print(chunk.text, end="")

generate()

