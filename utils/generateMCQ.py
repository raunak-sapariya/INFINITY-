import time
import json
from openai import OpenAI
import os

client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROK_API_KEY")
    )

def generateQuestion(para):
    data=""
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": '''Generate one array python of 2 multiple-choice questions in strict JSON format of {question:"question related to topic,options:one array of multile options to choose from,answer:"Correct answer" '} related to the following summary: '''+ para +" make sure the output is in JSON format and is strictly in the format mentioned above and does not contain any extra spaces or characters and valid JSON format"},
            {"role": "user", "content": para},
        ],
    )
    
    data=response.choices[0].message.content
    data_string = data.replace("'",'"').replace("```json", "").replace("```", "")
    return json.loads(data_string)
  