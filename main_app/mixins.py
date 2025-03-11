from django.shortcuts import redirect
from main_app.models import Group, Task, Task_User
from auth_app.models import User

class AdminOnly(object):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="admin").exists():
            return redirect('/?error=access_denied')
        return super().dispatch(request, *args, **kwargs)

class TeacherPanel_Group(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(id=self.kwargs.get('pk'))
            if not (self.request.user.groups.filter(name="admin").exists() or group.teacher == self.request.user):
                return redirect('/?error=access_denied')
        except:
            return redirect('main')
        return super().dispatch(request, *args, **kwargs)
    
class CourseViewAllow(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(id=self.kwargs.get('group_pk'))
            if not group.students.filter(id=self.request.user.id).exists():
                return redirect('/?error=access_denied')
        except:
            return redirect('main')
        return super().dispatch(request, *args, **kwargs)
    
class TaskViewAllow(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            group_pk = self.kwargs.get('group_pk')
            task_pk = self.kwargs.get('task_pk')
            user_pk = self.kwargs.get('user_pk')
            current_user = self.request.user
            if user_pk == 0:
                if not (current_user.groups.filter(name="admin").exists() or group.teacher == current_user):
                    return redirect('/?error=access_denied')
            else:
                group = Group.objects.get(id=group_pk)
                task = Task.objects.get(id=task_pk)
                user = User.objects.get(id=user_pk)
                t_u = Task_User.objects.get(task=task, user=user, group=group)
                if not (current_user.groups.filter(name="admin").exists() or group.teacher == current_user or t_u.user == current_user):
                    return redirect('/?error=access_denied')
        except:
            return redirect('main')
        return super().dispatch(request, *args, **kwargs)

class TeacherPanenViewAllow(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs.get('user_pk')
            if not (self.request.user.groups.filter(name="admin").exists() or User.objects.get(id=user_id) == self.request.user):
                return redirect('/?error=access_denied')
        except:
            return redirect('main')
        return super().dispatch(request, *args, **kwargs)