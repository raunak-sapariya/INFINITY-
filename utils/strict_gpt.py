
import openai
import re
import json
import concurrent.futures


openai.api_key = "YOUR-KEY-HERE"



def strict_output(system_prompt, user_prompt, output_format, model="gpt-4o-mini", temperature=0):
    
  
    
    response = openai.ChatCompletion.create(
        temperature=temperature,
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    generated_content = response['choices'][0]['message']['content']
    data_string = generated_content.replace("'", '"')

    return data_string





def process_prompt(prompt):
    system_prompt="You are an AI capable of curating course content, coming up with relevant consise chapter titles related to units given by user, and finding relevant youtube videos title for each chapter,and four hard quiz related to each chapter with four options and its correct answer "
    user_prompt=prompt
    output_format =  {"title":"consise title of unit","chapters":"an array of at least 5 chapters, each chapter should have a chapter 'title' key and 'youtube_query' key",
    }
    result = strict_output(system_prompt, user_prompt, output_format)
    return result



