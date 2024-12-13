from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import (Student,Teacher,TeachLeaveApp
                                ,StudentLeaveApp ,User, Admin,AppStatus)


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user


class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user

class AdminSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        student = Admin.objects.create(user=user)
        return user

class AppStatusForm(forms.ModelForm):
    class Meta:
        model = AppStatus

        fields = ('status',)

        widgets = {

            'status':forms.TextInput,

        }

class StdLeaveAppForm(forms.ModelForm):
    class Meta:
        model = StudentLeaveApp

        fields = ('content', 'to_teacher')
        labels = {
            'to_teacher': 'Send to which manager',
            'content': 'Please state your reason for your absence',
        }

        widgets = {

            'content': forms.TextInput,

        }

class TeachLeaveAppForm(forms.ModelForm):
    class Meta:
        model = TeachLeaveApp
        fields = ('content', 'to_admin',)
        labels = {
            'to_admin': 'Send to which HR',
            'content': 'Please state your reason for your absence',
        }

        widgets = {
            'content': forms.TextInput
        }
