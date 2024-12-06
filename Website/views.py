from django.shortcuts import render,redirect,HttpResponse
from django.http import StreamingHttpResponse,JsonResponse
from django.contrib import messages
from utils.strict_gpt import process_prompt
from utils.getImage import getImage
from utils.generateMCQ import generateQuestion
from utils.searchYoutube import searchYoutube,getCaption
import concurrent.futures
from django.views.decorators.csrf import csrf_exempt
from .models import Course,Unit,Chapter,Question
import time 
import json
from uuid import uuid4
from django.contrib.auth.decorators import login_required 
import json
import time

courses=[]

def home(req):
    return render(req,'home.html',{}) 

@login_required
def allCourses(req):
    
    currentUser=req.user
   
    courses=Course.objects.filter(userId=currentUser.id)
    allCourses=[]
    for course in courses:
        course={
            "id":course.id,
            "image":course.image,
            "name":course.name
        }
        allCourses.append(course)

    return render(req,"courses.html",{"courses":allCourses})
    
  
    

@login_required
def addCourse(req): 
    if req.method=="POST":
        data=json.loads(req.body.decode("utf-8"))
        courseName=data.get("courseName")
        unitNames=data.get("units")
        req.session["courseName"]=courseName
        courses.append((courseName,unitNames))
        return JsonResponse({"message":"done"})


@login_required
def streamUnit(req):
    
    if (len(courses)!=0):
      
        courseName=courses[0][0]
        unitNames=courses[0][1]
        units=[]
        for unit in unitNames:
            prompt="The User wants to learn about "+ courseName +". It is your job to create a course only about "+unit+", the User has requested to create chapters for each of the units. Then for each chapter, provide a detailed youtube search query that can be used to find informative educational video for each chapter. Each query should give an educational informative course in youtube"
            units.append(prompt)
        
   
        courses.pop(0)
      

        res=StreamingHttpResponse(streamHelper(units),content_type="text/event-stream")
        
        return res
    return redirect("/courses#add")


def process_prompt_with_retry(prompt):
    for attempt in range(5):
        try:
            result = process_prompt(prompt)
            data = json.loads(result.replace("'",'"').replace("```json", "").replace("```", "") )
            return data
        except json.JSONDecodeError as e:
            print(f"Attempt {attempt + 1} failed: line 81 {e}")
           

def streamHelper(units):

            
        with concurrent.futures.ThreadPoolExecutor() as exc:
            res = [exc.submit(process_prompt_with_retry, prompt) for prompt in units]
            for f in concurrent.futures.as_completed(res):
                data = f.result()
                if data is not None:
                    title = data["title"]
                    chapters = data["chapters"]
                    yield f"data:{json.dumps({"title": title, "chapters": chapters})}\n\n"
        

@login_required
def generateCourse(req,courseName):
    if len(courses)!=0:
        return render(req,"generateCourse.html",{"courseName":courseName})
    return redirect("/courses")


@login_required
def course(req,courseId):

    try:

        course=Course.objects.get(id=courseId)
        units=Unit.objects.filter(courseId=course.id)


        
    
        courseData={}
        courseData["title"]=course.name
        courseData["units"]=[]
        

        for unit in units:
            unitData={}
            unitData["title"]=unit.name
            unitData["chapters"]=[]
            chapters=Chapter.objects.filter(unitId=unit.id)
            for chapter in chapters:
                
                chapterData={}
                chapterData["Id"]=chapter.id
                chapterData["title"]=chapter.name
                chapterData["youtubeQuery"]=chapter.youtubeSearchQuery
                chapterData["videoId"]=chapter.videoId
                unitData["chapters"].append(chapterData)

                    

            courseData["units"].append(unitData)
        return render(req,"course.html",{"course":courseData})
    except:
        return redirect("/courses")






@csrf_exempt
def addCourseToDB(req):
    
    currentUser=req.user
    if (currentUser.username):
        data=json.loads(req.body.decode("utf-8"))
        courseName=data["courseName"]
        units=data["unitData"]
        if (courseName==""):
            return HttpResponse("{'mes':'Not found'}",status=400)
        if (len(units)!=3):

            return HttpResponse('{"mes":"Not found"}',status=400)
        
        try:
            courseImg=getImage(courseName)
        except:
            courseImg="https://imgs.search.brave.com/td8sI4KnqQOLjxGhhpHWvRi7r-MIvDsHtTEAMuTkGOw/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9pbWcu/ZnJlZXBpay5jb20v/cHJlbWl1bS1waG90/by9sZWFybmluZy1v/bmxpbmUtY29uY2Vw/dC15b3VuZy13b21h/bi11c2luZy1jb21w/dXRlci1sYXB0b3At/bGVhcm4tZS1sZWFy/bmluZy1jb3Vyc2Ut/ZnJvbS1pbnRlcm5l/dC1ob21lXzM0MDQ4/LTEyMDYuanBn"
        finally:
            course=Course(id=str(uuid4()),name=courseName.capitalize(),image=courseImg,userId=currentUser.id)
            course.save()
        
        for unit in units:
            newUnit=Unit(id=str(uuid4()),name=unit["title"],courseId=course.id,course=course)
            newUnit.save()

            for chapter in unit["chapters"]:
                newChapter=Chapter(id=uuid4(),unitId=newUnit.id,name=chapter["title"],youtubeSearchQuery=chapter["youtube_query"],unit=newUnit)
                newChapter.save()
            
            with concurrent.futures.ThreadPoolExecutor() as exc:
                print("===================================================================================================")
                res=[exc.submit(searchYoutube,chapter) for chapter in Chapter.objects.filter(unitId=newUnit.id)]
                
        return JsonResponse({"courseID":course.id})
                

    return HttpResponse("{'mes':'Not found'}",status=400)


    

@csrf_exempt
def getVideoSummary(req):
    chapterId=req.body.decode("utf-8")
    chapter=Chapter.objects.get(id=chapterId)
    

    
    
    if (chapter.summary):
        print(chapter.videoId)
        return JsonResponse({"summary":chapter.summary})
        
    chapter.summary=getCaption(chapter.videoId)
    chapter.save()

    return JsonResponse({"summary":chapter.summary})




@csrf_exempt
def getVideoQuestions(req):
    print("------------------------------------------------------------------------------------------------------")
    chapterId=req.body.decode("utf-8")
    chapter=Chapter.objects.get(id=chapterId)
    questions=Question.objects.filter(chapterId=chapter.id)


    
    if (questions):
        jsonQuestion=[]
        for question in questions:
            data={
                "question":question.question,
                "options":question.options,
                "answer":question.answer
            }
            jsonQuestion.append(data)

        return JsonResponse({"questions":jsonQuestion})

    generatedQuestions=generateQuestion(chapter.summary)
    print(generatedQuestions)   

    if (generatedQuestions==None):
        return JsonResponse({"message":"Failed"},status=400)
    
     
    for question in generatedQuestions:
        question=Question(id=str(uuid4()),chapterId=chapter.id,question=question["question"],answer=question["answer"],options=question["options"],chapter=chapter) 
        question.save()

    questions=Question.objects.filter(chapter=chapter)
    
    jsonQuestion=[]
    for question in questions:
        data={
            "question":question.question,
            "options":question.options,
            "answer":question.answer
        }
        jsonQuestion.append(data)
    return JsonResponse({"questions":jsonQuestion})


@csrf_exempt
def deleteCourse(req):
    if req.method == 'POST':

        data = json.loads(req.body)
        course_id = data.get('courseId')
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return JsonResponse({'status': 'success'})
        except Course.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Course not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def err(req,exc):
    return render(req,"404.html")
    