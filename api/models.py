from django.db import models

class Classrooms(models.Model):
    organization = models.CharField(max_length=200)

class Homeworks(models.Model):
    classroom = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    hw_name = models.CharField(max_length=200)


class Classroom_student(models.Model):
    classroom = models.CharField(max_length=200)
    student = models.CharField(max_length=200)

class Homework_student(models.Model):
    homework = models.CharField(max_length=200)
    student = models.CharField(max_length=200)
# Create your models here.
