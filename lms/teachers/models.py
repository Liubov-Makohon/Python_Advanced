import random

from django.db import models
from faker import Faker


class Teacher(models.Model):
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
    first_name = models.CharField(max_length=60, null=False)
    last_name = models.CharField(max_length=60, null=False)
    speciality = models.CharField(choices=list_speciality, max_length=40, null=False)

    def __str__(self):
        return f"{self.full_name()}, {self.speciality} ({self.id})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def generate_teachers(cls, count):
        faker = Faker()
        for _ in range(count):
            t = cls(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                speciality=random.choice(speciality),
            )
            t.save()
