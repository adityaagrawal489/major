from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('studentclick', views.studentclick_view),
path('studentlogin', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
path('studentsignup', views.student_signup_view,name='studentsignup'),
path('student-dashboard', views.student_course,name='student-dashboard'),
path('student-exam', views.student_exam_view,name='student-exam'),
path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
path('start-exam/<int:pk>', views.start_exam_view,name='start-exam'),

path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-result', views.view_result_view,name='view-result'),
path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('student-marks', views.student_marks_view,name='student-marks'),
#enter a classroom
path('join-classroom',views.jaishreeram,name='join-clasroom'),
path('student_particular_course/<int:pk>',views.student_particular_course,name='stud_par_course'),
path('student_course',views.student_course,name='student_course'),
path('attend_meeting/<int:pk>',views.attend_meeting,name='attend-meeting'),
path('all_students/<int:pk>',views.all_students,name='all_students')
]
