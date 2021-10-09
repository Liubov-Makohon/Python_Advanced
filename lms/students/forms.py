from django.core.exceptions import ValidationError
from django.forms import ModelForm

from students.models import Student




class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'birthdate']
        
        
        # def clean_email(self):
        #     email = self.cleaned_data['email']
        #
        #     if 'elon' in email.lower():
        #         raise ValidationError('No Elon, please!')
        #
        #     return  email
        # расширение джанги 