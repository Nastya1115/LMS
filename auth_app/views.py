from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from auth_app.forms import UserForm, UserAuthForm, User, ProfileForm
from django.views.generic import DetailView, UpdateView, DeleteView
from main_app.models import Group
from auth_app.mixins import UserIsProfileOwner
from django.contrib.auth.decorators import login_required
from main_app.mixins import AdminOnly
import os

DEFAULT_AVATAR_PATH = 'user_icons/standart_user.jpg'

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = UserForm()

    return render(
        request,
        template_name = 'auth/register.html',
        context = {'form': form}
    )

def login_user(request):
    if request.method == 'POST':
        form = UserAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
    else:
        form = UserAuthForm()

    return render(
        request,
        template_name = 'auth/login.html',
        context = {'form': form}
    )

@login_required
def logout_user(request):
    logout(request)
    return redirect('register')

class ProfileView(DetailView):
    model = User
    template_name = 'profile/profile.html'
    context_object_name = 'selected_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = self.get_object().group_set.all()
        return context
    
class UpdateProfileView(UserIsProfileOwner, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile/profile_update.html'
    context_object_name = 'selected_user'

    def form_valid(self, form):
        selected_object = self.get_object()
        avatar = form.cleaned_data.get('avatar')
        if selected_object.avatar != avatar and selected_object.avatar != DEFAULT_AVATAR_PATH:
            if os.path.isfile(selected_object.avatar.path):
                os.remove(selected_object.avatar.path)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})

class DeleteUserView(AdminOnly, DeleteView):
    model = User

    def get(self, request, *args, **kwargs):
        selected_object = self.get_object()
        if selected_object.avatar != DEFAULT_AVATAR_PATH:
            if os.path.isfile(selected_object.avatar.path):
                os.remove(selected_object.avatar.path)
        selected_object.delete()
        return redirect('admin_panel')