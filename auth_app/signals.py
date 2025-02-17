from django.db.models.signals import post_save
from django.dispatch import receiver
from auth_app.models import User
from django.contrib.auth.models import Group as RoleGroup

# Назначение статуса ученика
@receiver(post_save, sender=User)
def auto_student(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(RoleGroup.objects.get(id=3))