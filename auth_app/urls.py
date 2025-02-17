from django.urls import path
import auth_app.views as views

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("user/ban_user/<int:pk>/", views.DeleteUserView.as_view(), name="ban_user"),
    path("user/update_profile/<int:pk>/", views.UpdateProfileView.as_view(), name="update_profile"),
]