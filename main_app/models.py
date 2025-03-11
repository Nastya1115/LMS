from django.db import models
from auth_app.models import User
from urllib.parse import urlparse, parse_qs


TASK_TYPES = (
    ('VIDEO', 'video'),
    ('TEXT', 'text'),
    ('READ', 'read'),
)

class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=20, unique=True)
    desc = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='teaching_groups')
    students = models.ManyToManyField(User, blank=True)
    link = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, choices=(('OFFLINE', 'offline'),('ONLINE', 'online')))

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=20)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='tasks')
    type1 = models.CharField(max_length=20, choices=(('HW', 'Homework'),('CW', 'Classwork')))
    type2 = models.CharField(max_length=20, choices=TASK_TYPES, default='TEXT')
    file = models.FileField(upload_to='tasks_files/', blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    max_note = models.IntegerField()

    def cut_url(self):
        url = self.link
        if self.type2 == 'VIDEO':
            if "youtu.be" in url:
                self.link = url.split("/")[-1]
            elif "youtube.com" in url:
                query = urlparse(url).query
                self.link = parse_qs(query).get("v", [None])[0]
        elif self.type2 == 'READ':
            if "docs.google.com/presentation/d/" in url:
                self.link = url.split("/d/")[1].split("/")[0]
        else:
            return self.link

    def save(self, *args, **kwargs):
        if self.type2 == 'VIDEO' or self.type2 == 'READ':
            self.cut_url()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Task_User(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks_group')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_user')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tasks_task')
    is_complete = models.BooleanField(default=False)
    text = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    note = models.IntegerField(default=0)

    def __str__(self):
        return self.group.name + ' ' + self.user.username + ' ' + self.task.name

class Lesson_Group(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_groups')
    avaible = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name + ' ' + self.lesson.name
    
class CourseRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_requests')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_requests')
    email = models.EmailField()

    def __str__(self):
        return self.user.username + ' ' + self.course.name
    
class New(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_user')
    text = models.TextField()
    sender = models.ForeignKey(Lesson_Group, on_delete=models.CASCADE, related_name='notifications_sender')