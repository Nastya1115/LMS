from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from main_app.models import New, Course, Group, Module, Task, Lesson, Task_User, Tag, Lesson_Group, CourseRequest
from auth_app.models import User
from main_app.forms import NewForm, CourseForm, GroupForm, LessonForm, TagForm, ModuleForm, TaskStudentForm, TaskTeacherForm, TaskForm, CourseRequestForm
from django.http import HttpResponseRedirect
from django.forms import HiddenInput
from django.contrib.auth.models import Group as RoleGroup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main_app.mixins import AdminOnly, TeacherPanel_Group, CourseViewAllow, TeacherPanenViewAllow, TaskViewAllow
from django.urls import reverse_lazy
from django.db import models
import os


#####       TEMPLATE VIEW       #####

class MainPage(TemplateView):
    template_name = 'main/main_page.html'
    
class AdminPanelView(AdminOnly, TemplateView):
    template_name = 'admin/admin_panel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_search = self.request.GET.get('course_search')
        tag_search = self.request.GET.get('tag_search')
        group_search = self.request.GET.get('group_search')
        user_search = self.request.GET.get('user_search')
        context['courses_requests'] = CourseRequest.objects.all()
        context['news'] = New.objects.all()
        if course_search:
            context['courses'] = Course.objects.filter(name__icontains=course_search)
        else: 
            context['courses'] = Course.objects.all()
        if tag_search:
            context['tags'] = Tag.objects.filter(name__icontains=tag_search)
        else:
            context['tags'] = Tag.objects.all()
        if group_search:
            context['groups'] = Group.objects.filter(name__icontains=group_search)
        else:
            context['groups'] = Group.objects.all()
        if user_search:
            context['users'] = User.objects.filter(username__icontains=user_search)
        else:
            context['users'] = User.objects.all()
        return context
    
class TeacherPanelView(TeacherPanenViewAllow, TemplateView):
    template_name = 'teacher/teacher_panel.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('user_search')
        if username:
            try:
                user = User.objects.get(username=username)
                return redirect('teacher_panel', user_pk=user.id)
            except:
                pass
        return redirect('teacher_panel', user_pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_user'] = User.objects.get(id=self.kwargs.get('user_pk'))
        return context
    
class TaskView(TaskViewAllow, TemplateView):
    template_name = 'tasks/task_page.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_pk = self.kwargs.get('user_pk')
        if user_pk != 0 and user == User.objects.get(id=user_pk):
            task = Task.objects.get(id=self.kwargs.get('task_pk'))
            if task.type2 == 'VIDEO' or task.type2 == 'READ':
                meaningless_variable_name = self.get_task_user_obj()
                meaningless_variable_name.is_complete = True
                meaningless_variable_name.note = task.max_note
                meaningless_variable_name.save()
        return super().get(request, *args, **kwargs)

    def get_task_user_obj(self, *args, **kwargs):
        group = Group.objects.get(id=self.kwargs.get('group_pk'))
        task = Task.objects.get(id=self.kwargs.get('task_pk'))
        selected_user = User.objects.get(id=self.kwargs.get('user_pk'))
        return Task_User.objects.get(group=group, user=selected_user, task=task)
    
    def teacher_or_admin(self):
        if self.request.user.groups.filter(name="teacher").exists() or self.request.user.groups.filter(name="admin").exists():
            return True
        else:
            return False

    def post(self, request, *args, **kwargs):
        if self.kwargs.get('user_pk') != 0 and self.kwargs.get('group_pk') != 0:
            task = Task.objects.get(id=self.kwargs.get('task_pk'))
            if task.type2 == 'TEXT':        
                if self.request.user.groups.filter(name="student").exists():
                    task_form = TaskStudentForm(request.POST)
                    if task_form.is_valid():
                        task_user = self.get_task_user_obj()
                        task_user.text = task_form.cleaned_data['text']
                        task_user.save()
                        return HttpResponseRedirect(request.path)       
                elif self.teacher_or_admin():
                    task_form = TaskTeacherForm(request.POST)
                    if task_form.is_valid():
                        task_user = self.get_task_user_obj()
                        task_user.text = task_form.cleaned_data['text']
                        task_user.is_complete = task_form.cleaned_data['is_complete']
                        task_user.comment = task_form.cleaned_data['comment']
                        task_user.note = task_form.cleaned_data['note']
                        task_user.save()
                        return HttpResponseRedirect(request.path)
                
        return HttpResponseRedirect(request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.get(id=self.kwargs.get('task_pk'))
        context['task'] = task
        if task.type2 == 'TEXT':
            if self.kwargs.get('user_pk') == 0 or self.kwargs.get('group_pk') == 0:
                context['task_form'] = TaskStudentForm()
            else:
                initial_data = {}
                task_user = self.get_task_user_obj()
                context['task_user'] = task_user
                initial_data['text'] = task_user.text
                if self.request.user.groups.filter(name="student").exists():
                    context['task_form'] = TaskStudentForm(initial=initial_data)
                elif self.teacher_or_admin():
                    initial_data['is_complete'] = task_user.is_complete
                    initial_data['comment'] = task_user.comment
                    initial_data['note'] = task_user.note
                    context['task_form'] = TaskTeacherForm(initial=initial_data)
                    context['is_teacher'] = True
        return context

class StudentView(TeacherPanel_Group, TemplateView):
    template_name = 'teacher/student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = Group.objects.get(id=self.kwargs.get('pk'))
        context['group'] = group
        context['lesson_groups'] = Lesson_Group.objects.filter(group=group)
        context['student'] = User.objects.get(id=self.kwargs.get('user_pk'))
        return context

class CoursesView(TemplateView):
    template_name = 'courses/courses_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name_search = self.request.GET.get('name_search')
        tags_search = self.request.GET.get('tags_search', '').split()
        tags = list(Tag.objects.filter(name__in=tags_search))
        if name_search and tags:
            context['courses'] = (Course.objects.filter(name__icontains=name_search,tags__in=tags).annotate(count=models.Count("tags")).filter(count=len(tags)).distinct())
        elif name_search:
            context['courses'] = Course.objects.filter(name__icontains=name_search)
        elif tags:
            context['courses'] = (Course.objects.filter(tags__in=tags).annotate(count=models.Count("tags")).filter(count=len(tags)).distinct())
        else:
            context['courses'] = Course.objects.all()
        return context

class NewsView(TemplateView):
    template_name = 'main/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = New.objects.all()
        return context

#####       DETAIL VIEW       #####

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

class CourseView(CourseViewAllow, DetailView):
    model = Course
    template_name = 'courses/course_page.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks_user = Task_User.objects.filter(user=self.request.user)
        modules = self.get_object().modules.all()
        tasks = []
        for module in modules:
            for lesson in module.lessons.all():
                for task in lesson.tasks.all():
                    tasks.append(task)
        tasks_dict = {}
        for task in tasks:
            task_user = tasks_user.filter(task=task).first()
            if task_user:  
                tasks_dict[task] = task_user
            else:
                tasks_dict[task] = False
        context['modules'] = modules
        context['tasks_dict'] = tasks_dict
        context['group'] = Group.objects.get(id=self.kwargs.get('group_pk'))
        return context
    
class TGroupView(TeacherPanel_Group, DetailView):
    model = Group
    template_name = 'teacher/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_groups'] = Lesson_Group.objects.filter(group=self.get_object())
        return context
    
#####       CREATE VIEW       #####

class CreateCourseView(AdminOnly, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'admin/create_course.html'
    success_url = '/admin_panel/'

class CreateGroupView(AdminOnly, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'admin/create_group.html'
    success_url = '/admin_panel/'

    def form_valid(self, form):
        course_id = self.kwargs.get('course_pk')
        if course_id != 0:
            form.instance.course = Course.objects.get(id=course_id)
        else:
            course_name = form.cleaned_data.get('course_field')
            try:
                form.instance.course = Course.objects.get(name=course_name)
            except:
                form.add_error('course_field', 'Course does not exist!')
                return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_pk')
        context['course_check'] = course_id
        if course_id != 0:
            form = GroupForm(initial={'course_field': Course.objects.get(id=course_id)})
            form.fields['course_field'].widget = HiddenInput()
            context['form'] = form
        return context

class CreateNewView(AdminOnly, CreateView):
    model = New
    form_class = NewForm
    template_name = 'admin/create.html'
    context_object_name = 'selected_object'
    success_url = '/admin_panel/'

class CreateModuleView(AdminOnly, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'admin/create.html'
    context_object_name = 'selected_object'

    def get_success_url(self, **kwargs):
        return reverse_lazy('update_course', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form, *args, **kwargs):
        course_id = self.kwargs.get('pk')
        form.instance.course = Course.objects.get(id=course_id)
        return super().form_valid(form)
    
class CreateLessonView(AdminOnly, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'admin/create.html'
    context_object_name = 'selected_object'

    def get_success_url(self, **kwargs):
        return reverse_lazy('update_module', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form, *args, **kwargs):
        module_id = self.kwargs.get('pk')
        form.instance.module = Module.objects.get(id=module_id)
        return super().form_valid(form)

class CreateCourseRequestView(LoginRequiredMixin, CreateView):
    model = CourseRequest
    form_class = CourseRequestForm
    template_name = 'admin/create.html'
    success_url = '/courses/'
    context_object_name = 'selected_object'

    def form_valid(self, form):
        user = self.request.user
        course = Course.objects.get(id=self.kwargs.get('course_pk'))
        if CourseRequest.objects.filter(user=user, course=course).exists():
            form.add_error(None, "You already sent request on this course")
            return self.form_invalid(form)
        form.instance.user = user
        form.instance.course = course
        return super().form_valid(form)

class CreateTaskView(AdminOnly, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'admin/create.html'
    context_object_name = 'selected_object'

    def get_success_url(self, **kwargs):
        module = Lesson.objects.get(id=self.kwargs.get('lesson_pk')).module
        return reverse_lazy('update_module', kwargs={'pk': module.id})

    def form_valid(self, form, *args, **kwargs):
        lesson = Lesson.objects.get(id=self.kwargs.get('lesson_pk'))
        form.instance.lesson = lesson
        return super().form_valid(form)

#####       UPDATE VIEW       #####

class UpdateCourseView(AdminOnly, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'admin/update_course.html'
    context_object_name = 'course'

    def get_initial(self):
        initial = super().get_initial()
        initial['tags'] = ''
        return initial

    def form_valid(self, form):
        name_tags = form.cleaned_data.get('tags', '').split()
        for name_tag in name_tags:
            tag = Tag.objects.filter(name=name_tag).first()
            if tag:
                self.get_object().tags.add(tag)
            else:
                new_tag = Tag.objects.create(name=name_tag)
                self.get_object().tags.add(new_tag)
        return redirect('update_course', self.get_object().id)
    
class UpdateTagView(AdminOnly, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'admin/create.html'
    context_object_name = 'selected_object'
    success_url = '/admin_panel/'

class UpdateNewView(AdminOnly, UpdateView):
    model = New
    form_class = NewForm
    template_name = 'admin/create.html'
    context_object_name = 'selected_object'
    success_url = '/admin_panel/'

class UpdateModuleView(AdminOnly, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = 'admin/update_module.html'
    context_object_name = 'module'

    def get_success_url(self, **kwargs):
        return reverse_lazy('update_module', kwargs={'pk': self.kwargs.get('pk')})

class UpdateLessonView(AdminOnly, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'admin/create.html'
    context_object_name = 'selected_object'

    def get_success_url(self, **kwargs):
        return reverse_lazy('update_lesson', kwargs={'pk': self.kwargs.get('pk')})

class UpdateTaskView(AdminOnly, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'admin/create.html'
    context_object_name = 'task'

    def form_valid(self, form):
        selected_object = self.get_object()
        if selected_object.file:
            if os.path.isfile(selected_object.file.path):
                os.remove(selected_object.file.path)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('update_task', kwargs={'pk': self.kwargs.get('pk')})

class UpdateGroupView(AdminOnly, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'admin/update_group.html'
    context_object_name = 'group'

    def get_success_url(self, **kwargs):
        return reverse_lazy('update_group', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        usernames = form.cleaned_data.get('students_field', ' ').split()
        course_name = form.cleaned_data.get('course_field')
        teacher_name = form.cleaned_data.get('teacher_field')
        for username in usernames:
            try:
                group = self.get_object()
                selected_user = User.objects.get(username=username)
                group.students.add(selected_user)
                lss = group.lessons.all()
                for ls in lss:
                    if ls.avaible:
                        for task in ls.lesson.tasks.all():
                            if not Task_User.objects.filter(task=task, user=selected_user, group=group).exists():
                                Task_User.objects.create(task=task, user=selected_user, group=group)
            except:
                pass
        course = Course.objects.filter(name=course_name).first()
        teacher = User.objects.filter(username=teacher_name).first()
        if course:
            form.instance.course = course
        else:
            pass
        if teacher:
            form.instance.teacher = teacher
        else:
            pass
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['course_field'] = self.get_object().course
        initial['teacher_field'] = self.get_object().teacher
        return initial

#####       DELETE VIEW       #####

class DeleteNewView(AdminOnly, DeleteView):
    model = New

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect('admin_panel')

class DeleteCourseView(AdminOnly, DeleteView):
    model = Course

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect('admin_panel')
    
class DeleteTagView(AdminOnly, DeleteView):
    model = Tag

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect('admin_panel')
    
class DeleteModuleView(AdminOnly, DeleteView):
    model = Module

    def get(self, request, *args, **kwargs):
        course_pk = self.get_object().course.id
        self.get_object().delete()
        return redirect('update_course', pk=course_pk)

class DeleteLessonView(AdminOnly, DeleteView):
    model = Lesson

    def get(self, request, *args, **kwargs):
        module_pk = self.get_object().module.id
        self.get_object().delete()
        return redirect('update_module', pk=module_pk)

class DeleteTaskView(AdminOnly, DeleteView):
    model = Task

    def get(self, request, *args, **kwargs):
        selected_object = self.get_object()
        module_pk = self.get_object().lesson.module.id
        if selected_object.file:
            if os.path.isfile(selected_object.file.path):
                os.remove(selected_object.file.path)
        selected_object.delete()
        return redirect('update_module', pk=module_pk)

class DeleteGroupView(AdminOnly, DeleteView):
    model = Group

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect('admin_panel')

class DeleteCourseRequestView(AdminOnly, DeleteView):
    model = CourseRequest

    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return redirect('admin_panel')

#####       NON CLASS VIEWS       #####

@login_required
def change_theme(request):
    if request.method == 'GET':
        user = request.user
        if user.theme:
            user.theme = False
            user.save()
        else:
            user.theme = True
            user.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def unlock_lesson(request, lesson_pk, group_pk):
    if request.method == 'GET':
        if request.user.groups.filter(name="teacher").exists() or request.user.groups.filter(name="admin").exists():
            lesson = Lesson.objects.get(id=lesson_pk)
            group = Group.objects.get(id=group_pk)
            l_g = Lesson_Group.objects.get(group=group, lesson=lesson)
            if not l_g.avaible:
                l_g.avaible = True
                l_g.save()
                for user in group.students.all():
                    for task in lesson.tasks.all():
                        Task_User.objects.create(user=user, task=task, group=group)
    return redirect('tgroup_detail', pk=group_pk)

def make_admin(request, user_pk):
    if request.method == 'GET':
        if request.user.groups.filter(name="admin").exists(): 
            user = User.objects.get(id=user_pk)
            user.groups.remove(RoleGroup.objects.get(name="teacher"))
            user.groups.remove(RoleGroup.objects.get(name="student"))
            user.groups.add(RoleGroup.objects.get(name="admin"))
        return redirect('admin_panel')
    
def make_teacher(request, user_pk):
    if request.method == 'GET':
        if request.user.groups.filter(name="admin").exists(): 
            user = User.objects.get(id=user_pk)
            user.groups.remove(RoleGroup.objects.get(name="admin"))
            user.groups.remove(RoleGroup.objects.get(name="student"))
            user.groups.add(RoleGroup.objects.get(name="teacher"))
        return redirect('admin_panel')
    
def make_student(request, user_pk):
    if request.method == 'GET':
        if request.user.groups.filter(name="admin").exists(): 
            user = User.objects.get(id=user_pk)
            user.groups.remove(RoleGroup.objects.get(name="teacher"))
            user.groups.remove(RoleGroup.objects.get(name="admin"))
            user.groups.add(RoleGroup.objects.get(name="student"))
        return redirect('admin_panel')

def remove_user_from_group(request, group_pk, user_pk):
    if request.method == 'GET':
        if request.user.groups.filter(name="admin").exists():
            group = Group.objects.get(id=group_pk)
            user = User.objects.get(id=user_pk)
            group.students.remove(user)
    return redirect('update_group', pk=group_pk)