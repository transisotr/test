from google import genai
import os

# 输入提示词，生成代码，使用的gemini的模型是gemini-3-pro-preview，高级推理。

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

client = genai.Client(
    project="train-max-20260104",
    location="global",
)

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the meaning of life?"
)

print(result.embeddings)

# (base) PS D:\Download\ai-python> & D:/anaconda3/python.exe d:/Download/ai-python/week6/EmbeddingsDemo.py
# [ContentEmbedding(
#   statistics=ContentEmbeddingStatistics(
#     token_count=7.0,
#     truncated=False
#   ),
#   values=[
#     -0.022374553605914116,
#     -0.004560776986181736,
#     0.01330928597599268,
#     -0.05450719967484474,
#     -0.020904429256916046,
#     <... 3067 more items ...>,
#   ]
# )]