import os
import openai
import json
import re

openai.base_url = "https://api.groq.com/openai/v1 "
openai.api_key='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'

response = openai.ChatCompletion.create(
          temperature = .5,
          model="llama-3.1-70b-versatile",
          messages=[
            {"role": "system", "content": "You are AI"},
            {"role": "user", "content": "this is test"}
          ]
        )

res = response['choices'][0]['message']['content'].replace('\'', '"')
        
        
