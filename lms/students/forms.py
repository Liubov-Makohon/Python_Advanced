import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from students.models import Student


class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "birthdate"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        banned_email = [
            "@xyz.com",
            "@dot.com",
        ]
        for _ in banned_email:
            if _ in email:
                raise ValidationError("You can't use this email")

        return email

    def clean_birthdate(self):
        birthdate = self.cleaned_data["birthdate"]
        if datetime.datetime.now().year - birthdate.year < 18:
            raise ValidationError("Student must be 18 or older")

        return birthdate
