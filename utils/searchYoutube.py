from youtube_api import YouTubeDataAPI
from youtube_transcript_api import YouTubeTranscriptApi 
from uuid import uuid4
from openai import OpenAI
import requests
import time  
import json
import os


def searchYoutube(chapter):
    

    yt = YouTubeDataAPI(os.getenv("YOUTUBE_API_KEY"))
    search=yt.search(q=chapter.youtubeSearchQuery,max_results=15,video_duration="medium")
    print("--------------------------------------------------------------------------------------------------------------------",search)
    
    for i in range(len(search)):
        if (search[i]["channel_id"] not in ["UCBwmMxybNva6P_5VmxjzwqA","UCeVMnSShP_Iviwkknt83cww"]):
            try:
                script=YouTubeTranscriptApi.get_transcript(search[i]["video_id"]) 
                print("--------------------------------------------------------------------------------------------------",script)
                
                chapter.videoId=search[i]["video_id"]
                print(chapter)
                chapter.save()
                return chapter
            except Exception:
                pass

client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROK_API_KEY")
    )

def getCaption(id):
    print("-------------------------------------------------",id)
    summary=YouTubeTranscriptApi.get_transcript(id)
    print("----------------------------------------------------------------------------------------------------------------",summary)
    text=""
    for i in range(len(summary)):
        text+=summary[i]["text"]

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "make it a summary in html format use proper spacing and formatting and be consistant with the style in html format and make sure the summary is in html format and is strictly in the format mentioned above and does not contain any extra spaces or characters and valid html format and make sure the summary is in html format and is strictly in the format mentioned above and does not contain any extra spaces or characters and valid html format"},
            {"role": "user", "content": text},
        ],
    )
       
    return response.choices[0].message.content


