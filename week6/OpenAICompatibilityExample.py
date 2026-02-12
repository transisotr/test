import openai
from google.auth import default
from google.auth.transport.requests import Request
import os

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
# 在使用令牌之前，需要刷新凭据以获取一个有效的访问令牌。
# The google.auth.default() method returns credentials, but they need to be refreshed to get an access token.
credentials.refresh(Request())

client = openai.OpenAI(
    base_url=f"https://aiplatform.googleapis.com/v1/projects/{'train-max-20260104'}/locations/global/endpoints/openapi",
    api_key=credentials.token,
)

prompt = """
Write a bash script that takes a matrix represented as a string with
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

response = client.chat.completions.create(
    model="google/gemini-3-pro-preview",
    reasoning_effort="medium", # Map to thinking_level high.
    messages=[{"role": "user", "content": prompt}],
)

print(response.choices[0].message.content)