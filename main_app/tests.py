from django.test import TestCase
from main_app.models import Course, Group, Module, Task, Lesson, Task_User, Tag, Lesson_Group, CourseRequest, New
from auth_app.models import User
from main_app.signals import auto_connection_group_lessons_2, auto_connection_group_lessons_1, auto_connection_group_lessons_2
from auth_app.signals import auto_student
from django.db.models.signals import post_save

post_save.disconnect(auto_connection_group_lessons_1, sender=Group)
post_save.disconnect(auto_connection_group_lessons_2, sender=Lesson)
post_save.disconnect(auto_connection_group_lessons_2, sender=Task)
post_save.disconnect(auto_student, sender=User)

#####       MODELS       #####

class TagModelTest(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name='test_tag')
        self.assertEqual(tag.name, 'test_tag')
    
    def test_str(self):
        tag = Tag.objects.create(name='test_tag')
        self.assertEqual(str(tag), 'test_tag')

class CourseModelTest(TestCase):
    def test_create_course(self):
        course = Course.objects.create(name='test_course')
        self.assertEqual(course.name, 'test_course')
    
    def test_str(self):
        course = Course.objects.create(name='test_course')
        self.assertEqual(str(course), 'test_course')

class GroupModelTest(TestCase):
    def test_create_group(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        group = Group.objects.create(name='test_group', course=course)
        group.students.add(user)
        self.assertEqual(group.name, 'test_group')
        self.assertIn(user, group.students.all())
    
    def test_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        group = Group.objects.create(name='test_group', course=course)
        self.assertEqual(str(group), 'test_group')

class GroupModelTest(TestCase):
    def test_create_group(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        group = Group.objects.create(name='test_group', course=course)
        group.students.add(user)
        self.assertEqual(group.name, 'test_group')
        self.assertIn(user, group.students.all())
    
    def test_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        group = Group.objects.create(name='test_group', course=course)
        self.assertEqual(str(group), 'test_group')

class ModuleModelTest(TestCase):
    def test_create_module(self):
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        self.assertEqual(module.name, 'test_module')
    
    def test_str(self):
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        self.assertEqual(str(module), 'test_module')

class LessonModelTest(TestCase):
    def test_create_lesson(self):
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        lesson = Lesson.objects.create(name='test_lesson', module=module)
        self.assertEqual(lesson.name, 'test_lesson')
    
    def test_str(self):
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        lesson = Lesson.objects.create(name='test_lesson', module=module)
        self.assertEqual(str(lesson), 'test_lesson')

class TaskModelTest(TestCase):
    def test_create_task(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        lesson = Lesson.objects.create(name='test_lesson', module=module)
        task = Task.objects.create(
            name='test_task',
            desc='Test task description',
            lesson=lesson,
            type1='HW',
            type2='TEXT',
            max_note=10
        )
        self.assertEqual(task.name, 'test_task')
    
    def test_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        lesson = Lesson.objects.create(name='test_lesson', module=module)
        task = Task.objects.create(
            name='test_task',
            desc='Test task description',
            lesson=lesson,
            type1='HW',
            type2='TEXT',
            max_note=10
        )
        self.assertEqual(str(task), 'test_task')

class TaskUserModelTest(TestCase):
    def test_create_task_user(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        lesson = Lesson.objects.create(name='test_lesson', module=module)
        task = Task.objects.create(
            name='test_task',
            desc='Test task description',
            lesson=lesson,
            type1='HW',
            type2='TEXT',
            max_note=10
        )
        group = Group.objects.create(name='test_group', course=course)
        task_user = Task_User.objects.create(group=group, user=user, task=task, is_complete=False, note=7)
        self.assertEqual(task_user.is_complete, False)
        self.assertEqual(task_user.note, 7)
    
    def test_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        lesson = Lesson.objects.create(name='test_lesson', module=module)
        task = Task.objects.create(
            name='test_task',
            desc='Test task description',
            lesson=lesson,
            type1='HW',
            type2='TEXT',
            max_note=10
        )
        group = Group.objects.create(name='test_group', course=course)
        task_user = Task_User.objects.create(group=group, user=user, task=task, is_complete=False, note=7)
        self.assertEqual(str(task_user), 'test_group testuser test_task')

class LessonGroupModelTest(TestCase):
    def test_create_lesson_group(self):
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        lesson = Lesson.objects.create(name='test_lesson', module=module)
        group = Group.objects.create(name='test_group', course=course)
        lesson_group = Lesson_Group.objects.create(group=group, lesson=lesson, avaible=True)
        self.assertEqual(lesson_group.avaible, True)
    
    def test_str(self):
        course = Course.objects.create(name='test_course')
        module = Module.objects.create(name='test_module', course=course)
        lesson = Lesson.objects.create(name='test_lesson', module=module)
        group = Group.objects.create(name='test_group', course=course)
        lesson_group = Lesson_Group.objects.create(group=group, lesson=lesson, avaible=True)
        self.assertEqual(str(lesson_group), 'test_group test_lesson')

class CourseRequestModelTest(TestCase):
    def test_create_course_request(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        course_request = CourseRequest.objects.create(user=user, course=course, email='test@example.com')
        self.assertEqual(course_request.email, 'test@example.com')
    
    def test_str(self):
        user = User.objects.create_user(username='testuser', password='password')
        course = Course.objects.create(name='test_course')
        course_request = CourseRequest.objects.create(user=user, course=course, email='test@example.com')
        self.assertEqual(str(course_request), 'testuser test_course')

class NewModelTest(TestCase):
    def test_create_new(self):
        new = New.objects.create(title='test_title', text='test_text')
        self.assertEqual(new.title, 'test_title')
    
    def test_str(self):
        new = New.objects.create(title='test_title', text='test_text')
        self.assertEqual(str(new), 'test_title')

#####       VIEWS       #####

class MainPageTest(TestCase):
    def test_main_page_loads_correctly(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main_page.html')