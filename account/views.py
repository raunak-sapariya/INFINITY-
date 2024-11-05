from django.shortcuts import render,HttpResponse,redirect
import json
from django.contrib.auth.models import User 
from django.contrib import auth
import re
# Create your views here.

def register(req):
    user=req.user
    if user.is_authenticated:
       return redirect("/")
    
    if req.method =='POST':
       
       
       username=req.POST['f_name']
       email=req.POST['mail'].lower()
       password=req.POST['pass']
       
       if  len(username)<3 or len(username)>25:
          req.session['error']="Invalid username"
          return redirect("/register")
        
       regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
       if not (re.fullmatch(regex,email)):
           req.session['error']="Incorrect emaill"
           return redirect("/register")
       
       if  len(password)<8:
          req.session['error']="Invalid password"
          return redirect("/register")  
     


       if User.objects.filter(username=username).exists():
          
          req.session['error']="Username already taken"
          return redirect("/register")
          
       if User.objects.filter(email=email).exists():
         
          req.session['error']="Email already taken"
          return redirect("/register")
         
       else:   
        user=User(username=username,email=email,password=password)
        user.save()
        auth.login(req,user)

       response=redirect('/')
       
       return response
       #return render(req,'home.html')
    
    
    else:
     
     error=req.session.get("error","")
     req.session['error']=''
     return render(req,'registration/register.html',{"error":error})

def login(req):
    user=req.user
    if user.is_authenticated:
       return redirect("/")
    if req.method =='POST':
       
       
       email=req.POST['email'].lower()
       password=req.POST['password']
    

       regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
       if not (re.fullmatch(regex,email)):
           req.session['error']="Invalid Credentials"
           return redirect("/login")
       
       elif  len(password)<8:
          req.session['error']="Invalid Credentials"
          return redirect("/login")
       
      

       u=User.objects.filter(email=email)
       if u:
          username=u[0].username
          
          user=auth.authenticate(username=username,password=password)  

          if user is not None:
                auth.login(req,user)
                response=redirect('/')
                return response
          else:
                req.session['error']="Invalid Credentials"
                return redirect("/login")
       else:
            req.session['error'] = "Email does not exist."
            return redirect("/login")  
    
    else:
     error=req.session.get("error","")
     req.session['error']=''
     return render(req,'registration/login.html',{"error":error})






def logout(req):
   auth.logout(req)
   return redirect("/")
