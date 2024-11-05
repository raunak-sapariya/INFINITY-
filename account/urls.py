from django.urls import path
from . import views
from django.contrib.auth import views as vv



urlpatterns = [
    path('register/',views.register,name="a"),
    path('login/',views.login),
    path('logout/',views.logout),

    
]
