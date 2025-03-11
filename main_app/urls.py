from django.urls import path
import main_app.views as views

urlpatterns = [
    # global / panels / other / minor
    path("", views.MainPage.as_view(), name="main"),
    path("change_theme/", views.change_theme, name="change_theme"),
    path("admin_panel/", views.AdminPanelView.as_view(), name="admin_panel"),
    path("course_request/<int:course_pk>/", views.CreateCourseRequestView.as_view(), name="send_course_request"),
    path("course_request/delete/<int:pk>/", views.DeleteCourseRequestView.as_view(), name="delete_course_request"),
    path("teacher_panel/<int:user_pk>/", views.TeacherPanelView.as_view(), name="teacher_panel"),
    path("teacher_panel/student/<int:pk>/<int:user_pk>", views.StudentView.as_view(), name="student_view"),
    path("admin_panel/make_admin/<int:user_pk>/", views.make_admin, name="make_admin"),
    path("admin_panel/make_teacher/<int:user_pk>/", views.make_teacher, name="make_teacher"),
    path("admin_panel/make_student/<int:user_pk>/", views.make_student, name="make_student"),
    # notifications stuff
    path("notifications/", views.NotificationsView.as_view(), name="notifications_page"),
    path("notifications/delete/<int:notification_pk>/", views.delete_notification, name="delete_notification"),
    path("notifications/delete_all/", views.delete_all_notification, name="delete_all_notification"),
    # news stuff
    path("news/", views.NewsView.as_view(), name="news"),
    path("news/add_new/", views.CreateNewView.as_view(), name="new_new"),
    path("news/update_new/<int:pk>/", views.UpdateNewView.as_view(), name="update_new"),
    path("news/delete_new/<int:pk>/", views.DeleteNewView.as_view(), name="delete_new"),
    # course stuff
    path("courses/", views.CoursesView.as_view(), name="courses"),
    path("course/<int:pk>/", views.CourseDetailView.as_view(), name="courses_detail"),
    path("course/<int:pk>/group/<int:group_pk>/", views.CourseView.as_view(), name="course_view"),
    path("course/add_course/", views.CreateCourseView.as_view(), name="new_course"),
    path("course/update_course/<int:pk>/", views.UpdateCourseView.as_view(), name="update_course"),
    path("course/delete_course/<int:pk>/", views.DeleteCourseView.as_view(), name="delete_course"),
    # lesson stuff
    path("lesson/unlock/<int:lesson_pk>/<int:group_pk>/", views.unlock_lesson, name="unlock_lesson"),
    path("module/<int:pk>/lesson/add_lesson/", views.CreateLessonView.as_view(), name="new_lesson"),
    path("lesson/update_lesson/<int:pk>/", views.UpdateLessonView.as_view(), name="update_lesson"),
    path("lesson/delete_lesson/<int:pk>/", views.DeleteLessonView.as_view(), name="delete_lesson"),
    # group stuff
    path("group/add_group/<int:course_pk>/", views.CreateGroupView.as_view(), name="new_group"),
    path("group/update_group/<int:pk>/", views.UpdateGroupView.as_view(), name="update_group"),
    path("group/delete_group/<int:pk>/", views.DeleteGroupView.as_view(), name="delete_group"),
    path("teacher_panel/group/<int:pk>/", views.TGroupView.as_view(), name="tgroup_detail"),
    path("group/remove_student/<int:group_pk>/<int:user_pk>/", views.remove_user_from_group, name="remove_student"),
    # module stuff
    path("course/<int:pk>/add_module/", views.CreateModuleView.as_view(), name="new_module"),
    path("module/update_module/<int:pk>/", views.UpdateModuleView.as_view(), name="update_module"),
    path("module/delete_module/<int:pk>/", views.DeleteModuleView.as_view(), name="delete_module"),
    # tag stuff
    path("tag/update_tag/<int:pk>/", views.UpdateTagView.as_view(), name="update_tag"),
    path("tag/delete_tag/<int:pk>/", views.DeleteTagView.as_view(), name="delete_tag"),
    # task stuff
    path("task/add_task/<int:lesson_pk>/", views.CreateTaskView.as_view(), name="add_task"),
    path("task/update_task/<int:pk>/", views.UpdateTaskView.as_view(), name="update_task"),
    path("task/delete_task/<int:pk>/", views.DeleteTaskView.as_view(), name="delete_task"),
    path("group/<int:group_pk>/task/<int:task_pk>/user/<int:user_pk>/", views.TaskView.as_view(), name="task_view"),
]