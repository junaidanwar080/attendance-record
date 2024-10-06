from django.contrib import admin
from django.urls import path, include
from attandance import views
urlpatterns = [
    # path('index/', views.index, name='index'),  
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    # path('register_student/', views.register_student, name='register_student'),
    # path('register_list/', views.register_list, name='register_list'),
    # path('update_register/<int:user_id>/', views.update_register, name='update_register'),
    # designation
    path('designation_add/', views.designation_add , name = 'designation_add'),
    path('designation_list/', views.designation_list , name = 'designation_list'),
    path('designation_update/<int:designation_id>/', views.designation_update, name='designation_update'),
    path('<int:pk>/designation_delete/', views.designation_delete , name = 'designation_delete'),
    # DEPARTMENT
    path('department_add/', views.department_add , name = 'department_add'),
    path('department_list/', views.department_list , name = 'department_list'),
    path('department_update/<int:department_id>/', views.department_update, name='department_update'),
    path('<int:pk>/department_delete/', views.department_delete , name = 'department_delete'),
    # courses
    path('courses_add/', views.courses_add , name = 'courses_add'),
    path('courses_list/', views.courses_list , name = 'courses_list'),
    path('courses_update/<int:courses_id>/', views.courses_update, name='courses_update'),
#    class
    path('classes_add/', views.classes_add , name = 'classes_add'),
    path('classes_list/', views.classes_list , name = 'classes_list'),
    path('classes_update/<int:class_id>/', views.classes_update, name='classes_update'),
    
    
    path('student_list/', views.student_list , name = 'student_list'),
    path('add_student/', views.add_student , name = 'add_student'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('get_courses/', views.get_courses, name='get_courses'),
    
#    Teacher
    path('teacher_list/', views.teacher_list , name = 'teacher_list'),
    path('add_teacher/', views.add_teacher , name = 'add_teacher'),
    path('edit_teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    path('get_courses/', views.get_courses, name='get_courses'),
    path('upload_and_filter_attendance/', views.upload_and_filter_attendance, name='upload_and_filter_attendance'),
    # path('upload-excel/', views.upload_and_parse_excel, name='upload_excel'),
     path('view_profile/', views.view_profile, name='view_profile'),
    path('view_courses/', views.view_courses, name='view_courses'),
    path('view_attendance/', views.view_attendance, name='view_attendance'), 
    # path('check-task-status/', views.check_task_status, name='check-task-status'),
]  

