from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from students.models import Student
from students.utils import format_records

def hello(request):
    return HttpResponse('SUCCESS')



def get_students(request, first_name):

    students = Student.objects.all()

    if first_name:
        students = students.filter(first_name=first_name)

    result = format_records(students)

    return HttpResponse('GET STUDENTS')