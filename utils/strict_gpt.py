from openai import OpenAI
import re
import json
import concurrent.futures
import google.generativeai as genai
import os



def strict_output(system_prompt, user_prompt, output_format):
    
    # genai.configure(api_key=os.getenv("GOOGLE_GEMINI"))
    # model = genai.GenerativeModel("gemini-1.5-flash")

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROK_API_KEY")
    )

    system_prompt += f"Generate a strictly formatted JSON output adhering exactly to the provided format: {output_format}. Ensure the output is: (1) strictly compliant with the specified structure, (2) free of any unnecessary spaces, extra characters, or deviations, and (3) valid JSON with correct syntax. The output must conform precisely to the provided format without exceptions."

    # system_prompt += f"Generate a strict list of JSON data adhering to the specified format: {output_format}. Ensure the output is in valid JSON, precisely follows the given format, and contains no unnecessary spaces, characters, or deviations."

    # system_prompt += f"Generate strict list of JSON data in the following format: {output_format} without any unneccesssary space and valid json format."
    # system_prompt += "make sure the output is in JSON format and is strictly in the format mentioned above and does not contain any extra spaces or characters and valid JSON format"

    # print(system_prompt+user_prompt)
    # response = model.generate_content(system_prompt+user_prompt)

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    generated_content = response.choices[0].message.content
    data_string = generated_content.replace("'",'"').replace("```json", "").replace("```", "") 
    print(data_string)

    return data_string


def process_prompt(prompt):
    system_prompt="You are an AI capable of curating course content, coming up with relevant consise chapter titles related to units given by user, and finding relevant youtube videos title for each chapter."
    user_prompt=prompt
    output_format =  {"title":"consise title of unit","chapters":"an array of at least 5 chapters, each chapter should have a chapter 'title' key and 'youtube_query' key",
    }
    result = strict_output(system_prompt, user_prompt, output_format)
    return result



