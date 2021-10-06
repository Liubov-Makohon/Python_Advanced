from django.db import models


class Teacher(models.Model):
    first_name = models.CharField(max_length=60, null=False)
    last_name = models.CharField(max_length=60, null=False)
    speciality = models.CharField(max_length=80, null=False)
    faculty = models.CharField(max_length=80, null=False)
