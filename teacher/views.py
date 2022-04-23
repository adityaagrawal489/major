from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta

# from quiz import models as QMODEL
# from student import models as SMODEL
from quiz import forms as QFORM
from quiz.models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('teacherlogin')
    return render(request,'teacher/teachersignup.html',context=mydict)



def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict={
    
    'total_course':Course.objects.all().count(),
    'total_question':Question.objects.all().count(),
    'total_student':Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm=QFORM.CourseForm()
    if request.method=='POST':
        courseForm=QFORM.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request,'teacher/teacher_add_exam.html',{'courseForm':courseForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = Course.objects.all()
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request,'teacher/teacher_add_question.html',{'questionForm':questionForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses= Course.objects.all()
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def join_course(request):
   if request.method=='POST':
       
       classname=request.POST['classname']
       course=Course(course_name=classname)
       course.save()
       print(request.user.id)
      
       teacher=Teacher.objects.get(user_id=request.user.id)
       print(teacher)
       teacher.Course_id.add(course)
       return HttpResponseRedirect('teacher-dashboard')
   return render(request,'teacher/createclassroom.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_course(request):
    # courses=Course.objects.filter(pk=request.user.id)
    teacher=Teacher.objects.get(user_id=request.user.id)
    courses=teacher.Course_id.all()
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
    return render(request,'teacher/teacher_course.html',{'courses':courses,'name':request.user.username})
def teacher_particular_course(request,pk):
     if request.method=='POST':
          meeting =request.POST['meeting']
          start=request.POST['start']
          
          end_tim =request.POST['finish']
          dat= request.POST['date']
          try:
                meet=Meeting(Course_id_id=pk,Meeting_link=meeting,start_time=start,end_time=end_tim,date=dat)
                meet.save()
          except:
              print('something is wrong')
          AllMeeting=Meeting.objects.filter(Course_id=pk)
          return render(request,'teacher/nabar_testing.html',{'name':pk,'Meeting':AllMeeting})
 
     AllMeeting=Meeting.objects.filter(Course_id=pk)
     name=pk
     print(AllMeeting)
     return render(request,'teacher/nabar_testing.html',{'name':pk,'Meeting':AllMeeting})

def teacher_create_meeting(request):
    meeting =request.post['meeting']
    start=request.post['start']
    end =request.post['end']
    date= request.post['date']
    return render(request,'teacher/nabar_testing.html' )
    
def  teacher_student_attendence(request,pk):
    totals=Meeting.objects.filter(Course_id=pk).count()
    Allmeeting=Meeting.objects.filter(Course_id=pk)
    Allmeeting=list(map((lambda x:x.id),Allmeeting))
    
    students=Student.objects.filter(Course=pk)
    print(Allmeeting)
    attedance=list(map((lambda x:particular_student(x,Allmeeting)),students)) 
    print(attedance)
    print(students)
    print(totals)
    mylist = zip(students, attedance)
    
                
            
    return render(request,'teacher/attendence.html',{'name':pk,'mylist':mylist,'total':totals})

def particular_student(student,All):
     print('jaishreepram',All)
     print('its is user id',student.user_id)
     anshuman=Attendence.objects.filter(meeting_id__in=All)
     
     return Attendence.objects.filter(student_id=student,meeting_id__in=All).count()

def all_students(request,pk):
    students=Student.objects.filter(Course=pk)
    teachers=Teacher.objects.filter(Course_id=pk)
    print(teachers)
    print(students)
    return render(request,'teacher/students.html',{'name':pk,'students':students,'teachers':teachers}) 

