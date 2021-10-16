import random

from django.db import models


class Group(models.Model):
    list_speciality = [
        ("Anesthesiology", "Anesthesiology"),
        ("Dermatology", "Dermatology"),
        ("Neurology", "Neurology"),
        ("Ophthalmology", "Ophthalmology"),
        ("Pathology", "Pathology"),
        ("Pediatrics", "Pediatrics"),
        ("Psychiatry", "Psychiatry"),
        ("Surgery", "Surgery"),
        ("Urology", "Urology"),
    ]
    speciality = models.CharField(choices=list_speciality, max_length=40, null=False)
    year_of_entry = models.IntegerField(null=False)
    group_number = models.IntegerField(null=False)

    def __str__(self):
        return (
            f"{self.speciality}, {self.year_of_entry}, {self.group_number} ({self.id})"
        )

    @classmethod
    def generate_groups(cls, count):
        year_of_entry = list(range(2015, 2022))
        for _ in range(count):
            gr = cls(
                speciality=random.choice(speciality),
                year_of_entry=random.choice(year_of_entry),
                group_number=random.randrange(3),
            )
            gr.save()
