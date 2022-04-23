import re
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import uuid


class Course(models.Model):
   join_code = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField(null=True)
   total_marks = models.PositiveIntegerField(null=True)
   starttime=models.DateTimeField(blank=True, null=True)
   endtime=models.DateTimeField(blank=True,null=True)
   totaltime = models.IntegerField(null=True, blank=True, default=100, help_text="duration of the quiz in minutes")
   def __str__(self):
        return self.course_name
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)
    Course_id=models.ManyToManyField(Course,blank=True,null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    Course=models.ManyToManyField('Course',related_name='Anshuman',blank=True,null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name


class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=RichTextField()
    questionimg=models.ImageField(upload_to='image/', default='image/noimage.png', null=True, blank=True)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class Meeting(models.Model):
    Course_id=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    Meeting_link=models.CharField(max_length=20,blank=True,)
    start_time=models.TimeField()
    end_time=models.TimeField()
    date=models.DateField()
    class Meta:
      unique_together = ('start_time', 'end_time','date','Course_id')
class  Attendence(models.Model):
    meeting_id=models.ForeignKey(Meeting,on_delete=models.DO_NOTHING)
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
      
    
class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

