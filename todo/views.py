from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import Tasks
from django.shortcuts import get_object_or_404


def signup_view(request):
    if(request.method=='POST'):
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        print(uname,pwd)

        if(User.objects.filter(username=uname).exists()):
            # means username already exists
            msg = "Username already exists"
            return render(request,'signup.html',{'msg':msg})
        
        user = User.objects.create_user(username=uname,password=pwd)
        user.save()
        request.session["user_id"] = user.id
        print('I am saving details into the database')
        msg = "Account Created Successfully! Please Login!"
        return render(request,'signup.html',{'msg':msg})
    return render(request,'signup.html',{})

def login_view(request):
    if(request.method=='POST'):
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        print(uname,pwd)
        user = authenticate(request,username=uname,password=pwd)
        if user:
            print("i am in inside if-block")
            z = login(request,user)
            print(z)
            #messages.success(request,"Login ")
            print("Same block,i am going to home page")

            return redirect('home')
        else:
            print(user)
            print("I am insidde else-block")
            err_msg = "Invalid Crdentials"
            return render(request,'login.html',{'result':err_msg})

    return render(request,'login.html',{})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    task_obj = Tasks.objects.filter(user=request.user)
    return render(request,'home.html',{'data':task_obj})

@login_required
def addtask_view(request):
    print("I just entered into the function")
    if(request.method=='POST'):
        print("I am the request with POST")
        task = request.POST.get('task')
        deadline = str(request.POST.get('deadline')).lower()

        # check in database for data duplication if any,  comment-1
        print("I am the line below at comment-1")
        # if(Tasks.objects.filter(taskname=task).exists()):
        #     taskmsg = "task Already Exists"
        #     print("I am inside the duplication if condition,So i am returning")
        #     return render(request,'addtask.html',{'taskmsg':taskmsg})

        # Task enetered is not in database comment-2
        print("I am the line below comment -2")
        print("deadline = ",deadline)
        #deadline = deadline[::-1]
        todaydate = str(timezone.now())
        todaydate = todaydate[:10]
        todayarr = todaydate.split('-')
        deadlinearr = deadline.split('-')
        print("today = ",todaydate)
        print("deadline = ",deadline)
        todayday = todayarr[0]
        todaymonth = todayarr[1]
        todayyear = todayarr[2]
        dlday = deadlinearr[0]
        dlmonth = deadlinearr[1]
        dlyear = deadlinearr[2]
        
        print("================",Tasks.objects.filter(taskname=task).exists())
        print("-=-=-=-=-=-=-=-=",todaydate == deadline)
        if(Tasks.objects.filter(taskname=task).exists() and todaydate == deadline): # Means task already exists and on the same date
            print("--------------- i am here------------------------- ")
            taskmsg = "task Already Exists"
            print("I am inside the duplication if condition,So i am returning")
            return render(request,'addtask.html',{'taskmsg':taskmsg})

        #date valid condition comment-3
        print("I am the line below comment-3")
        if (int(todayyear) > int(dlyear)) or (int(todaymonth) > int(dlyear)) or (int(todayday) > int(dlday)) :
            errmsg = "Invalid date"
            print(" I am inside the date valid condition ,So i am returning ")
            return render(request,'addtask.html',{'errmsg':errmsg}) # eg: 2025 > 2023 return false type


        if task is not None: #means user has enetered some data,other than None comment-4
            print(" I am the line in the ,if the task is not none , below the comment-4")
            task = request.POST.get('task')
            date = str(timezone.now())
            deadline = request.POST.get("deadline")
            task_obj = Tasks.objects.create(user=request.user)
            task_obj.user = request.user
            task_obj.taskname = task
            task_obj.date = date
            task_obj.deadline = deadline
            task_obj.save()
            msg = "Task Added Succesfully!"
            return render(request,'addtask.html',{'smsg':msg})
        else:
            msg = "Please Enter Valid Task!"
            return render(request,"addtask.html",{'msg':msg})
    return render(request,'addtask.html',{})

@login_required
def edittask_view(request,taskid):
    task = get_object_or_404(Tasks,pk=taskid)
    if(request.method=='POST'):
        taskname = request.POST.get('taskname')
        deadline = request.POST.get('deadline')
        task.taskname = taskname
        task.deadline = deadline
        task.save()
        messages.success(request,'Changes Updated Successfully!')
        return redirect('home')
    return render(request,'edittask.html',{'task':task})

@login_required
def delete_view(request,taskid):
    task = get_object_or_404(Tasks,pk=taskid)
    task.delete()
    return redirect('home')