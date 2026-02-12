from google import genai
from google.genai.types import (
    HttpOptions,
    Tool,
    ToolCodeExecution,
    GenerateContentConfig,
)
import os

# 根据描述生成代码

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

client = genai.Client(
    project="train-max-20260104",
    location="global",
    http_options=HttpOptions(api_version="v1")
)

model_id = "gemini-2.5-flash"

code_execution_tool = Tool(code_execution=ToolCodeExecution())
response = client.models.generate_content(
    model=model_id,
    contents="Calculate 20th fibonacci number. Then find the nearest palindrome to it.",
    config=GenerateContentConfig(
        tools=[code_execution_tool],
        temperature=0,
    ),
)
print("# Code:")
print(response.executable_code)
print("# Outcome:")
print(response.code_execution_result)


# Example response:
# # Code:
# def fibonacci(n):
#     if n <= 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         a, b = 0, 1
#         for _ in range(2, n + 1):
#             a, b = b, a + b
#         return b
#
# fib_20 = fibonacci(20)
# print(f'{fib_20=}')
#
# # Outcome:
# fib_20=6765