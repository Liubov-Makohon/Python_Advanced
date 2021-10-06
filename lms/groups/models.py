from django.db import models


class Group(models.Model):
    faculty = models.CharField(max_length=80, null=False)
    speciality = models.CharField(max_length=80, null=False)
    year_of_entry = models.IntegerField(max_length=4, null=False)
    group_number = models.IntegerField(max_length=1, null=False)
