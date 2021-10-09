import random

from django.db import models


class Group(models.Model):
    speciality = models.CharField(max_length=80, null=False)
    year_of_entry = models.IntegerField(null=False)
    group_number = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.speciality}, {self.year_of_entry}, {self.group_number} ({self.id})'

    @classmethod
    def generate_groups(cls, count):
        speciality = ['Anesthesiology', 'Dermatology', 'Neurology', 'Ophthalmology', 'Pathology', 'Pediatrics', 'Psychiatry', 'Surgery', 'Urology']
        year_of_entry = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
        for _ in range(count):
            gr = cls(
                speciality=random.choice(speciality),
                year_of_entry=random.choice(year_of_entry),
                group_number=random.randrange(3),
            )
            gr.save()
