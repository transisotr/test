import os
from google import genai
from google.genai.types import HttpOptions
from google.genai import types

# 调用模型聊天

# This environment variable is crucial to tell the google-genai library
# to use the Vertex AI backend, which enables authentication via ADC.
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# 由于您安装的 google-genai 库版本较旧，没有 genai.configure() 方法。
# 我们将 project 和 location 直接传递给 Client 构造函数，以使用 Vertex AI 和 ADC。
client = genai.Client(
    project="train-max-20260104",  
    location="global",             
    http_options=HttpOptions(api_version="v1")
)
response = client.models.generate_content(
    # 模型
    model="gemini-2.5-flash",
    # 上下文
    contents="你是怎么工作的？",
    # 生成配置
    config=types.GenerateContentConfig(
        # 思考等级
       thinking_config=types.ThinkingConfig(
           # LOW,HIGH，【MEDIUM，MINIMAL（仅限 Gemini 3 Flash）】
           thinking_level=types.ThinkingLevel.LOW # For fast and low latency response
       )
   ),
)
print(response.text)
# Example response:
# Okay, let's break down how AI works. It's a broad field, so I'll focus on the ...
#
# Here's a simplified overview:
# ...


