from django.urls import path
from . import views




urlpatterns = [
    path('',views.home,name="home"),
    path('addCourse/',views.addCourse,name="addCourse"),
    path('course/<str:courseId>/', views.course, name='course'),
    path('courses/', views.allCourses, name='allCourse'),
    path('streamUnit/', views.streamUnit, name='allCourse'),
    path('courses/<str:courseName>', views.generateCourse, name='allCourse'),
    path("addToDB/",views.addCourseToDB),
    path("getVideoSummary/",views.getVideoSummary),
    path("getVideoQuestions/",views.getVideoQuestions),
    path('deleteCourse/', views.deleteCourse),



]

handler404=views.err