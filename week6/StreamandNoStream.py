from google import genai
from google.genai import types
import os
from google.genai.types import HttpOptions

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# 流式请求会在处理过程中分块返回响应。对于用户而言，流式响应可以降低延迟感知。
def generateStream():

#   client = genai.Client(vertexai=True, api_key=YOUR_API_KEY)

  client = genai.Client(
        project="train-max-20260104",  
        location="global",             
        http_options=HttpOptions(api_version="v1")
  )

  config=types.GenerateContentConfig(
      temperature=0,
      top_p=0.95,
      top_k=20,
      candidate_count=1,
      seed=5,
      max_output_tokens=100,
      stop_sequences=["STOP!"],
      presence_penalty=0.0,
      frequency_penalty=0.0,
      safety_settings=[
          types.SafetySetting(
              category="HARM_CATEGORY_HATE_SPEECH",
              threshold="BLOCK_ONLY_HIGH",
          )
      ],
  )
  for chunk in client.models.generate_content_stream(
    model="gemini-2.5-flash-lite",
    contents="Explain bubble sort to me",
    config=config,
  ):
    print(chunk.text)


# 非流式请求则会在处理完毕后一次性返回响应。
def generatenoStream():
  client = genai.Client(
        project="train-max-20260104",  
        location="global",             
        http_options=HttpOptions(api_version="v1")
  )

  config=types.GenerateContentConfig(
      temperature=0,
      top_p=0.95,
      top_k=20,
      candidate_count=1,
      seed=5,
      max_output_tokens=100,
      stop_sequences=["STOP!"],
      presence_penalty=0.0,
      frequency_penalty=0.0,
      safety_settings=[
          types.SafetySetting(
              category="HARM_CATEGORY_HATE_SPEECH",
              threshold="BLOCK_ONLY_HIGH",
          )
      ],
  )
  response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Explain bubble sort to me",
    config=config,
  )
  print(response.text)

# 以下代码示例声明了一个函数并将其作为工具传递，然后在响应中接收函数调用部分。从模型接收到函数调用部分后，您可以调用该函数并获取响应，然后将响应传递给模型。
def functionsgen():
    client = genai.Client(
        project="train-max-20260104",  
        location="global",             
        http_options=HttpOptions(api_version="v1")
    )
    
    function_response_parts = [
        {
            'function_response': {
                'name': 'get_current_weather',
                'response': {
                    'name': 'get_current_weather',
                    'content': {'weather': 'super nice'},
                },
            },
        },
    ]
    manual_function_calling_contents = [
        {'role': 'user', 'parts': [{'text': 'What is the weather in Boston?'}]},
        {
            'role': 'model',
            'parts': [{
                'function_call': {
                    'name': 'get_current_weather',
                    'args': {'location': 'Boston'},
                }
            }],
        },
        {'role': 'user', 'parts': function_response_parts},
    ]
    function_declarations = [{
        'name': 'get_current_weather',
        'description': 'Get the current weather in a city',
        'parameters': {
            'type': 'OBJECT',
            'properties': {
                'location': {
                    'type': 'STRING',
                    'description': 'The location to get the weather for',
                },
                'unit': {
                    'type': 'STRING',
                    'enum': ['C', 'F'],
                },
            },
        },
    }]
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=manual_function_calling_contents,
        config=dict(tools=[{'function_declarations': function_declarations}]),
    )
    print(response.text)


# generateStream()
# generatenoStream()
functionsgen()