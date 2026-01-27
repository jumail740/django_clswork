from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from .models import *

def index(request):
    if request.user.is_authenticated:  
        stds= Students.objects.all()
        return render(request,'index.html',{'stds':stds})
    else:
        return redirect(loginUser)
    
    
def addstudent(request):
    courses=Courses.objects.all()
    if request.method=='POST':
      name=request.POST['name']
      email=request.POST['email']
      age= request.POST['age']
      phone=request.POST['phone']
      course= request.POST['course']
      cname=Courses.objects.get(cname=course)
      data=Students.objects.create(name=name,email=email,age=age,phone=phone,cname=cname)
      data.save
      
      return redirect(index)
    return render(request,'addstudent.html',{'courses':courses})


def editStudents(request,pk):
    std=Students.objects.get(pk=pk)
    courses= Courses.objects.all()
    if request.method=='POST':
      name=request.POST['name']
      email=request.POST['email']
      age= request.POST['age']
      phone=request.POST['phone']
      course= request.POST['course']
      cname=Courses.objects.get(cname=course)
      Students.objects.filter(pk=pk).update(name=name,email=email,age=age,phone=phone,cname=cname)
      return redirect(index)
    return render(request,'editStudents.html',{'std':std ,'courses':courses})

def deleteStudents(request,pk):
    Students.objects.get(pk=pk).delete()
    return redirect(index)

def registerUser(request):
    if request.method=='POST':
        name=request.POST['first_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cnf_password=request.POST['cnf_password']
        # print(name,username,email,password,cnf_password)
        if password==cnf_password:
            data = User.objects.create_user(first_name=name,username=username,email=email,password=password)
            data.save()
        else:
            print("password doesnot match")
    return render(request,'register.html')



def loginUser(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect(index)
        else:
            return redirect(loginUser)
    return render(request,'login.html')

def logoutUser(request):
    
    logout(request)
    return redirect(loginUser)