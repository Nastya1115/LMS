from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from main_app.models import Group, Task, Lesson_Group, Lesson, Task_User
from auth_app.models import User

# Если создается группа
@receiver(post_save, sender=Group)
def auto_connection_group_lessons_1(sender, instance, created, **kwargs):
    if created:
        for module in instance.course.modules.all():
            for lesson in module.lessons.all():
                Lesson_Group.objects.create(group=instance, lesson=lesson)

# Если создается урок
@receiver(post_save, sender=Lesson)
def auto_connection_group_lessons_2(sender, instance, created, **kwargs):
    if created:
        for group in Group.objects.filter(course=instance.module.course):
            Lesson_Group.objects.create(group=group, lesson=instance)

# Если создается задание
@receiver(post_save, sender=Task)
def auto_connection_group_lessons_2(sender, instance, created, **kwargs):
    if created:
        lesson = instance.lesson
        lesson_groups = lesson.lesson_groups.all()
        for l_g in lesson_groups:
            group = l_g.group
            if l_g.avaible:
                for user in group.students.all():
                    Task_User.objects.create(user=user, task=instance, group=group)

def create_super_user(sender, **kwargs):
    try:
        if not User.objects.get(username="admin"):
            User.objects.create(username="admin",password="43tg43yayayeyuse5y43t43tt4yhes5ususu5u56uj6tde5")
    except:
        pass