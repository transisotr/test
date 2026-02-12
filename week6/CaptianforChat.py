from google import genai
from google.genai import types
import os
from google.genai.types import HttpOptions

def generate():
  
  os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

  # 1. 更新客户端初始化方式，与其他示例保持一致
  client = genai.Client(
    vertexai=True,
    # 可以通过key来快速使用vertex AI，而不用需要繁琐的项目信息等配置。
    #   api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
    project="train-max-20260104",  
    location="global",             
    http_options=HttpOptions(api_version="v1")
  )

  # 2. 定义 variable1 变量
  variable1 = """You are Captain Barktholomew, the most feared pirate dog of the seven seas.
You were born in the 1700s and have no knowledge of anything that happened or
existed after that. Only talk about topics that a pirate dog captain would be
interested in."""

  model = "gemini-3-pro-preview"
  contents = [
    types.Content(
      role="user",
      parts=[
        # 3. 使用 f-string 将变量注入到提示中
        # types.Part.from_text(text="""{variable1}Hello! Do you like computers?""")
        types.Part.from_text(text=f"""{variable1}Hello! Do you like computers?""")
      ]
    ),
  ]
  tools = [
    types.Tool(google_search=types.GoogleSearch()),
  ]

  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
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
    tools = tools,
    thinking_config=types.ThinkingConfig(
      # 4. 使用枚举类型以确保类型安全
      thinking_level=types.ThinkingLevel.HIGH,
    ),
  )

  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
        continue
    print(chunk.text, end="")

generate()