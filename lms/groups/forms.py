from django.forms import ModelForm

from groups.models import Group


class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ["speciality", "year_of_entry", "group_number"]
