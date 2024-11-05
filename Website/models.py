from django.db import models


class Course(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    userId=models.IntegerField(null=True, blank=True)
    


class Unit(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    courseId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    course = models.ForeignKey('Course', on_delete=models.CASCADE,related_name='units')
    
    


class Chapter(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    unitId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    youtubeSearchQuery = models.CharField(max_length=255)
    videoId = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=3000, blank=True, null=True)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE,related_name='chapters')





class Question(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    chapterId = models.CharField(max_length=255)
    question = models.CharField(max_length=3000)
    answer = models.CharField(max_length=3000)
    options = models.CharField(max_length=3000)
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE, related_name='questions')
    

