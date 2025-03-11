from django.contrib import admin
from main_app.models import Course, Group, Module, Task, Lesson, Task_User, Tag, Lesson_Group, CourseRequest, New, Notification


admin.site.register(Course)
admin.site.register(Group)
admin.site.register(Module)
admin.site.register(Task)
admin.site.register(Lesson)
admin.site.register(Task_User)
admin.site.register(Tag)
admin.site.register(Lesson_Group)
admin.site.register(CourseRequest)
admin.site.register(New)
admin.site.register(Notification)