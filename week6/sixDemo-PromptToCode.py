import os
from google import genai
from google.genai import types
from google.genai.types import HttpOptions

# 输入提示词，生成代码，使用的gemini的模型是gemini-3-pro-preview，高级推理。

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

client = genai.Client(
    project="train-max-20260104",
    location="global",
    # http_options=HttpOptions(api_version="v1")
)

prompt = """
You are tasked with implementing the classic Thread-Safe Double-Checked Locking (DCL) Singleton pattern in modern C++. This task is non-trivial and requires specialized concurrency knowledge to prevent memory reordering issues.

Write a complete, runnable C++ program named `dcl_singleton.cpp` that defines a class `Singleton` with a private constructor and a static `getInstance()` method.

Your solution MUST adhere to the following strict constraints:
1. The Singleton instance pointer (`static Singleton*`) must be wrapped in `std::atomic` to correctly manage memory visibility across threads.
2. The `getInstance()` method must use `std::memory_order_acquire` when reading the instance pointer in the outer check.
3. The instance creation and write-back must use `std::memory_order_release` when writing to the atomic pointer.
4. A standard `std::mutex` must be used only to protect the critical section (the actual instantiation).
5. The `main` function must demonstrate safe, concurrent access by launching at least three threads, each calling `Singleton::getInstance()`, and printing the address of the returned instance to prove all threads received the same object.
"""

response = client.models.generate_content(
  model="gemini-3-pro-preview",
  contents=prompt,
  config=types.GenerateContentConfig(
      thinking_config=types.ThinkingConfig(
          thinking_level=types.ThinkingLevel.HIGH # Dynamic thinking for high reasoning tasks
      )
  ),
)

# 将生成的代码写入 .cpp 文件
generated_text = response.text
output_dir = "output_folder"
output_filename = os.path.join(output_dir, "dcl_singleton.cpp")

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 从 Markdown 代码块中提取纯代码
code_content = generated_text
if generated_text.strip().startswith("```cpp"):
    # 找到代码块的起始和结束位置
    code_start = generated_text.find('\n') + 1
    code_end = generated_text.rfind("```")
    if code_end != -1:
        code_content = generated_text[code_start:code_end].strip()

with open(output_filename, "w", encoding="utf-8") as f:
    f.write(code_content)

print(f"代码已成功保存到文件: {output_filename}")

