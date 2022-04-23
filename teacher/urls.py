from django.urls import path
from student.views import all_students
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teachersignup', views.teacher_signup_view,name='teachersignup'),
path('teacher-dashboard', views.teacher_course,name='teacher-dashboard'),
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),


path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('remove-question/<int:pk>', views.remove_question_view,name='remove-question'),
path('teacher-join-course',views.join_course,name='teacherjoin'),
path('teacher_courses',views.teacher_course,name='teachercourse'),
path('teacher_meeting',views.teacher_create_meeting,name='teachermeeting'),
# path('teacher_delete_course',views.teacher_delete_course,name='delete_course'),
path('teacher_particular_course/<int:pk>',views.teacher_particular_course,name='tea_par_course'),
path('teacher_student_attendence/<int:pk>',views.teacher_student_attendence,name='teacherstudent_attendence'),
path('all_teacher/<int:pk>',views.all_students,name='all_ts')
]