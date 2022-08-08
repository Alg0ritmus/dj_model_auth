from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import regForm, loginForm, createGroup

# for reg
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
# restrict pages

from django.contrib.auth.decorators import login_required

# mydec
from .decorators import allowedFor

# page restrictions:
# superuser > admin > tierThree > tierTwo > tierOne

# rules:
# If signed up for 1 time -> obtain tierOne
# "Buy" tierTwo (smth-like-VIP)
# "Buy+restriction(e.g. income)"

# Create your views here.
def home(request):
    tiers=""
    for i in request.user.groups.all():
        tiers+=i.name+", "

    return render(request,'base/index.html',{'tiers':tiers})


# allowedFor decorator is used to restrict page
# and make them available for particular groups
# note that user can have multiple groups with 
# different permissions, so it is very important
# to choose those permissions wisely

# also: u can generate diffrent HTML tags based
# on those permissions -> {% if user.has_perm..%}

# note that there are couple of methods to restrict
# only particular item from model (let say Model Shoes)
# has obj in db with name="nike shoes", u can restrict
# acces to that particular obj using django-guardian
@login_required
@allowedFor(['admin'])
def onlyAdmin(request):
    return HttpResponse("onlyAdmin page")

@login_required
def tierOne(request):
    return HttpResponse("tierOne page")

@login_required
@allowedFor(['admin','tierTwo','tierThree'])
def tierTwo(request):
    return HttpResponse("tierTwo page")

@login_required
@allowedFor(['admin','tierThree'])
def tierThree(request):
    return HttpResponse("tierThree page")

# LOG & REG pages

def loginPage(request):
    context={
        'form':loginForm()
    } 

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('base:home')
        else:
            print('smthing goes wrong')

    return render(request,'base/login.html',context)

def regPage(request):
       
    context={
        'form':regForm()
    }

    if request.method == 'POST':
        filledInForm = regForm(request.POST)
        if filledInForm.is_valid():
            def_group = Group.objects.get(name="tierOne")
            user = User.objects.create_user(username=request.POST['username'],
            password = request.POST['password'],email=request.POST['email'])
            user.groups.add(def_group)
            user.save()
            return redirect('base:loginPage')
        else:
            print("form is not valid",filledInForm.errors)
        


    return render(request,'base/reg.html',context)

def logoutPage(request):
    logout(request)
    return redirect('base:loginPage')

@login_required
@allowedFor(['admin'])
def createGroups(request):
    context={
        'group_form': createGroup(),
    }
    if request.method == 'POST':
        filledForm=createGroup(request.POST)
        if filledForm.is_valid():
            filledForm.save()
    
    return render(request,'base/group.html',context)

