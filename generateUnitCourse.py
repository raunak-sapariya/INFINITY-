from openai import OpenAI
import json
import re


client = OpenAI(
      base_url="https://api.groq.com/openai/v1",
      api_key="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"
  )

response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {"role": "system", "content": "You are an AI assistant."},
        {"role": "user", "content": "dbddd"}
    ],
)


