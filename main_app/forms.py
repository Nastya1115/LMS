from django import forms
from django.forms import ImageField, FileInput
from main_app.models import Course, Group, Lesson, Tag, Module, Task_User, Task, CourseRequest, New


class CourseForm(forms.ModelForm):
    tags = forms.CharField(required=False, max_length=256)
    class Meta:
        model = Course
        fields = ['name','desc','tags']

class GroupForm(forms.ModelForm):
    students_field = forms.CharField(required=False)
    course_field = forms.CharField()
    teacher_field = forms.CharField(required=False)
    class Meta:
        model = Group
        fields = ['name', 'link', 'type']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name']

class TaskForm(forms.ModelForm):
    file = ImageField(widget=FileInput(attrs={'id': 'image_input'}), required= False)
    class Meta:
        model = Task
        fields = ['name', 'desc', 'type1', 'type2', 'file', 'link', 'max_note']

class TaskStudentForm(forms.ModelForm):
    class Meta:
        model = Task_User
        fields = ['text']

class TaskTeacherForm(forms.ModelForm):
    class Meta:
        model = Task_User
        fields = ['text', 'is_complete', 'comment', 'note']

class CourseRequestForm(forms.ModelForm):
    class Meta:
        model = CourseRequest
        fields = ['email']

class NewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = ['title', 'text']