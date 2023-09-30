from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import Tripform,Taskform,Friendform
from django.contrib.auth import login,logout,authenticate
from .models import trip,tasks,friend
# Create your views here.
def home(request):
    return render(request,"sbill/home.html")

def completed(request,trip_pk):
    if request.method=='POST':
        trips=trip.objects.get(id=trip_pk)
        trips.delete()
        return redirect('currentpage')
def signupuser(request):
    if request.method=='GET':
        return render(request,'sbill\signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currentpage')
            except IntegrityError:
                return render(request,'sbill\signupuser.html',{'form':UserCreationForm(),'error':"Username Already Exists"})
        else:
            return render(request,'sbill\signupuser.html',{'form':UserCreationForm(),'error':"Password Didn't Match"})

def loginuser(request):
    if request.method=='GET':
        return render(request,'sbill\loginuser.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user==None:
            return render(request,'sbill\loginuser.html',{'form':AuthenticationForm(),'error':"Username or password is incorrect"})
        else:
            login(request,user)
            return redirect('currentpage')

def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

def currentpage(request):
    trips=request.user.trip_set.all()
    return render(request,'sbill\currentpage.html',{'trips':trips})

def addtrip(request):
    if request.method=='GET':
        return render(request,'sbill/trip1.html',{'form':Tripform()})
    else:
        form=Tripform(request.POST)
        newtrip = form.save(commit=False)
        newtrip.user_id=request.user
        newtrip.save()
        newtrip.user.add(User.objects.get(username=request.user))
        newtrip.save()
        return redirect('currentpage')

def addfriend(request,task_pk):
    if request.method=='GET':
        return render(request,'sbill/addfriend.html',{'form':Friendform()})
    else:
        form=Friendform(request.POST)
        newfriend = form.save(commit=False)
        newfriend.user_id=task_pk
        users=User.objects.all()
        trips=trip.objects.get(id=task_pk)
        fl=[]
        for i in users:
            a=0
            fl.append(i.username)
        if newfriend.friends in fl:
            newfriend.save()
            u1=User.objects.get(username=newfriend.friends)
            trips.user.add(u1)
            trips.save()
            return redirect('trippage',task_pk)
        else:
            return render(request,'sbill/addfriend.html',{'form':Friendform(),'error':"Friend name is incorrect/not found"})

def addtask(request,task_pk):
    tp={}
    tp["tp1"]=task_pk
    if request.method=='GET':
        return render(request,'sbill/task1.html',{'form':Taskform(),'tps':tp})
    else:
        form=Taskform(request.POST)
        newtask=form.save(commit=False)
        newtask.trip_name1_id=task_pk
        users=User.objects.all()
        fl=[]
        for i in users:
            a=0
            fl.append(i.username)
        if newtask.whopaid in fl:
            newtask.save()
            return redirect('trippage',task_pk)
        else:
            return render(request,'sbill/task1.html',{'form':Taskform(),'tps':tp,'error':"''Whopaid''  field is incorrect/not found from the members list"})

def trippage(request,task_pk):
    task = tasks.objects.filter(trip_name1 = task_pk)
    tp={}
    tp["tp1"]=task_pk
    friends=friend.objects.filter(user=task_pk)
    trips=trip.objects.filter(user=request.user)
    exp={}
    frnd=[]
    #creating a list with members
    for i in friends:
        exp[i.friends]=0
        frnd.append(i.friends)
    #creating a dictionary [member:total_amt_he_spent]
    for i in task:
        if(i.whopaid in exp):
            exp[i.whopaid]+=i.taskexp
    #each person's share
    rlt=[]
    for i in range(len(frnd)):
        for j in range(i+1,len(frnd)):
            diff_amt=exp[frnd[i]]//len(frnd)-exp[frnd[j]]//len(frnd)
            if diff_amt>0:
                rlt.append(str(frnd[j]+" owes "+frnd[i]+" RS."+str(diff_amt)))
            elif diff_amt<0:
                rlt.append(str(frnd[i]+" owes "+frnd[j]+" RS."+str(0-diff_amt)))
    return render(request,'sbill/trippage.html',{'tasks':task,'tps':tp,'friends':friends,'trips':trips,'exps':exp,'result':rlt})

def updatetask(request,trip_pk,task_pk):
    task=get_object_or_404(tasks,pk=task_pk)
    if request.method=='GET':
        return render(request,'sbill/updatetask.html',{'form':Taskform(instance=task)})
    else:
        try:
            form=Taskform(request.POST,instance=task)
            form.save()
            return redirect('trippage',trip_pk)
        except ValueError:
            return render(request,'sbill/updatetask.html',{'form':Taskform(instance=task),'error':"entered data is incorrect"})
