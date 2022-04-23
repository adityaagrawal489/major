from http.client import HTTPResponse
from django.shortcuts import render,redirect,reverse

from student.start_face_recognition import start_face_recognition
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
from . import start_face_recognition
import random
from random import shuffle
from quiz.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from . import capture_photos,create_folder,train_model
#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            new_user = authenticate(username=userForm.cleaned_data['username'],
                                    password=userForm.cleaned_data['password'],
                                    )
            login(request, new_user)
            request.session["FACE_PAGE"]=0
            return redirect('face_register')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    # total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    total_questions=course.question_number
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=course.total_marks
    # for q in questions:
    #     total_marks=total_marks + q.marks

    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questioncount=course.question_number
    questions=QMODEL.Question.objects.all().filter(course=course)
    shufflequestions=list(questions)
    shuffle(shufflequestions)
    shufflequestions=shufflequestions[0:questioncount]
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':shufflequestions})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view-result')



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def jaishreeram(request):
    if request.method=='POST':
       print(request.user.id)
       code=(request.POST['classroom'])
       course=Course.objects.get(join_code=code)
       student=Student.objects.get(user_id=request.user.id)
       student.Course.add(course)
       return HttpResponseRedirect('student-dashboard')
    return render(request,'student/join_course.html')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_course(request):
    # courses=Course.objects.filter(pk=request.user.id)
    student=Student.objects.get(user_id=request.user.id)
    courses=student.Course.all()
    # course=[
    #     {
    #       'title':'chemistry',
    #       'teacher':'sahuji'
    #     },
    #     {
    #        'title':'mathes',
    #        'teacher':'sharmaji'
    #     },
    #     {
    #        'title':'Genetic Algorithm',
    #        'teacher':'vermaji'
    #     },
    #     {
    #        'title':'Genetic Algorithm',
    #        'teacher':'vermaji'
    #     }
    # ]
    print(request.user.username)
    print(courses)
    return render(request,'student/student_course.html',{'courses':courses,'name':request.user.username})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_particular_course(request,pk):
     
     AllMeeting=Meeting.objects.filter(Course_id=pk)
     print(AllMeeting)
     return render(request,'student/nabar_testing.html',{'name':pk,'Meeting':AllMeeting})
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def teacher_create_meeting(request):
    meeting =request.post['meeting']
    start=request.post['start']
    end =request.post['end']
    date= request.post['date']
    return render(request,'teacher/nabar_testing.html' )
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def attend_meeting(request,pk):
    meeting=Meeting.objects.get(id=pk)
    print(meeting.start_time)
    print(meeting.end_time)
    start_time=str(meeting.start_time)
    end_time=str(meeting.end_time)
    student=Student.objects.get(user_id=request.user.id)
    print(request.user.id)
    attendance=Attendence(meeting_id=meeting,student_id=student)
    if(start_face_recognition.start_face_recognition(str(request.user.id),0,start_time,end_time)):
         attendance.save()
   
    return redirect('student_course')  
@login_required(login_url='studentlogin')
@user_passes_test(is_student)  
def all_students(request,pk):
    students=Student.objects.filter(Course=pk)
    teachers=Teacher.objects.filter(Course_id=pk)
    print(teachers)
    print(students)
    return render(request,'student/students.html',{'name':pk,'students':students,'teachers':teachers}) 

#shashank code
def send_mail(name,mail,request):
    import random
    num = str(random.randrange(100000, 999999))
    request.request.session["OTP"] = num
    #send_otp.send_mail(name,mail,num)
    return True

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def face_register(request):
    # print(request.session)
    # if request.session["FACE_PAGE"] == 0:
    #     request.session["cam_type"] = request.form["exampleRadios"]
    #     folder_loc = request.session["USERID"]+"/"
    #     create_folder.create_folder(folder_loc)
    #     request.session["FACE_PAGE"]=1
    #     return render("face_registeration_1.html")

        
    # if request.session["FACE_PAGE"] == 1:
    #     capture_photos.capture_photos(5,request.session["cam_type"],request.session["USERID"])
    #     #openCamera.open_cam(request.session["cam_type"])
    #     request.session["FACE_PAGE"]=2
    #     return render("face_registeration_2.html")

    # if request.session["FACE_PAGE"] == 2:
    #     capture_photos.capture_photos(5,request.session["cam_type"],request.session["USERID"])
    #     request.session["FACE_PAGE"]=3
    #     return render("face_registeration_3.html")

    # if request.session["FACE_PAGE"] == 3:
    #     capture_photos.capture_photos(5,request.session["cam_type"],request.session["USERID"])
    #     train_model.train_model(request.session["USERID"])
    #     return redirect(url_for("home"))
    # return render("home.html")
    if request.method=="POST":
        print(request.session["FACE_PAGE"])
        yeeroj=str(request.user.id)
        cam_type=0
        if request.session["FACE_PAGE"] == 0:
            
            request.session["cam_type"]=int(request.POST["exampleRadios"])
            folder_loc =yeeroj+"/"
            create_folder.create_folder(folder_loc)
            request.session["FACE_PAGE"]=1
            return render(request,"student/face_registeration_1.html")
        if request.session["FACE_PAGE"] == 1:
            capture_photos.capture_photos(5, request.session["cam_type"],yeeroj)
            #openCamera.open_cam(request.session["cam_type"])
            request.session["FACE_PAGE"]=2
            return render(request,"student/face_registeration_2.html")
        if request.session["FACE_PAGE"] == 2:
            capture_photos.capture_photos(5, request.session["cam_type"],yeeroj)
            request.session["FACE_PAGE"]=3
            return render(request,"student/face_registeration_3.html")
        if request.session["FACE_PAGE"] == 3:
            capture_photos.capture_photos(5, request.session["cam_type"],yeeroj)
            train_model.train_model(yeeroj)
            return redirect('student_course')
        student=Student.objects.get(id=request.user.id)
        user=User.objects.get(id=student.user_id)
        user.delete()
        student.delete()
        return redirect('student_click')
    return render(request,'student/face.html')

       

    