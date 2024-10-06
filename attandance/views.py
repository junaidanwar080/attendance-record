from django.shortcuts import render, redirect,get_object_or_404, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .tasks import *
from .helper import *
from datetime import datetime
x = datetime.now()  
date = x.strftime('%Y-%m-%d')
x = datetime.now()
y = x.strftime('%Y-%m-%d')
from django.utils import timezone
import pandas as pd
from django.utils.timezone import now
from datetime import datetime

# def index(request):
#     send_mail_task.delay() 
#     return HttpResponse("<h1>Home,from celery</h1>")


def home(request):
    return render(request,'before_login/home.html')
# -----------------------------------------------------------------------------------------------------
# Dashboard ,  admin
# -----------------------------------------------------------------------------------------------------


@login_required(login_url='home')
def dashboard(request):   
    return render(request, 'dashboard.html')
def teacher_dashboard(request):   
    return render(request, 'teacher/teacher_dashboard.html')

# def teacher_dashboard(request):
#     if request.user.is_authenticated:
#         try:
#             student = Student.objects.get(student_id=request.user)
#         except Student.DoesNotExist:
#             student = None

#         if student:
#             department = student.department
#             courses = student.courses.all()
#             classes = Classes.objects.filter(courses__in=courses)
#             context = {
#                 'student': student,
#                 'department': department,
#                 'courses': courses,
#                 'classes': classes,
#             }
#         else:
#             context = {'message': 'No student profile found.'}
        
#         return render(request, 'student/student_dashboard.html', context)
#     else:
#         return redirect('login')



# -----------------------------------------------------------------------------------------------------
# Student Account
# -----------------------------------------------------------------------------------------------------


@login_required(login_url='home')
def add_student(request):
    if request.method == "POST":
        last_student = Student.objects.order_by('-created_at').first()
        student_id = 1 if last_student is None else int(last_student.student_id) + 1

        error_messages = {}
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        department_id = request.POST.get('department')
        selected_courses = request.POST.getlist('courses')
        
        if not username:
            error_messages['username'] = "First Name is required."
        if not last_name:
            error_messages['last_name'] = "Last Name is required."
        if not email:
            error_messages['email'] = "Email is required."
        elif Student.objects.filter(email=email).exists():
            error_messages['email'] = "Email must be unique."
        if not password:
            error_messages['password'] = "Password is required."
        if not department_id:
            error_messages['department'] = "Department is required."

        if error_messages:
            departments = Department.objects.all()
            courses = Courses.objects.all()
            return render(request, 'admin/student_account/add_std_account.html', {
                'error_messages': error_messages,
                'form_data': request.POST,
                'student_id': student_id,
                'departments': departments,
                'courses': courses
            })

        student = Student(
            student_id=student_id,
            username=username,
            last_name=last_name,
            email=email,
            password=password, 
            department_id=department_id,
        )
        student.save()

        if selected_courses:
            student.courses.set(selected_courses)

        return redirect('student_list')

    last_student = Student.objects.order_by('-created_at').first()
    student_id = 1 if last_student is None else int(last_student.student_id) + 1

    departments = Department.objects.all()
    courses = Courses.objects.all()

    return render(request, 'admin/student_account/add_std_account.html', {
        "student_id": student_id,
        'departments': departments,
        'courses': courses,
    })

@login_required(login_url='home')
def student_list(request):  
    student = Student.objects.prefetch_related('courses').all()
    return render(request , 'admin/student_account/list_std_account.html', { 'student':student })

@login_required(login_url='home')
def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id) 

    if request.method == "POST":
        error_messages = {}
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        department_id = request.POST.get('department')
        selected_courses = request.POST.getlist('courses')

        if not username:
            error_messages['username'] = "First Name is required."
        if not last_name:
            error_messages['last_name'] = "Last Name is required."
        if not email:
            error_messages['email'] = "Email is required."
       
        if not password:
            error_messages['password'] = "Password is required."
        if not department_id:
            error_messages['department'] = "Department is required."

        if error_messages:
            departments = Department.objects.all()
            courses = Courses.objects.all()
            return render(request, 'admin/student_account/update_std_account.html', {
                'error_messages': error_messages,
                'form_data': request.POST,
                'student': student,
                'departments': departments,
                'courses': courses,
                'selected_courses': selected_courses
            })

        student.username = username
        student.last_name = last_name
        student.email = email
        student.password = password
        student.department_id = department_id
        
        student.save()
        
        if selected_courses:
            student.courses.set(selected_courses)
        
        return redirect('student_list')

    departments = Department.objects.all()
    courses = Courses.objects.all()
    selected_courses = list(student.courses.values_list('id', flat=True))

    return render(request, 'admin/student_account/update_std_account.html', {
        'student': student,
        'departments': departments,
        'courses': courses,
        'selected_courses': selected_courses
    })


def get_courses(request):
    department_id = request.GET.get('department_id')
    courses = Courses.objects.filter(department_id=department_id).values('id', 'name')
    return JsonResponse({'courses': list(courses)})

# -----------------------------------------------------------------------------------------------------
# Teacher Account
# -----------------------------------------------------------------------------------------------------
@login_required(login_url='home')
def add_teacher(request):
    if request.method == "POST":
        last_teacher = Teacher.objects.order_by('-created_on').first()
        teacher_id = 1 if last_teacher is None else int(last_teacher.teacher_id) + 1

        error_messages = {}
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        department_id = request.POST.get('department')
        designation_id = request.POST.get('designation')
        selected_courses = request.POST.getlist('courses')

        # Validation logic
        if not username:
            error_messages['username'] = "Username is required."
        if not last_name:
            error_messages['last_name'] = "Last Name is required."
        if not email:
            error_messages['email'] = "Email is required."
        elif Teacher.objects.filter(email=email).exists():
            error_messages['email'] = "Email must be unique."
        if not password:
            error_messages['password'] = "Password is required."
        if not department_id:
            error_messages['department'] = "Department is required."
        if not designation_id:
            error_messages['designation'] = "Designation is required."

        if error_messages:
            departments = Department.objects.all()
            designations = Designation.objects.all()
            courses = Courses.objects.all()
            return render(request, 'admin/teacher_account/add_tec_account.html', {
                'error_messages': error_messages,
                'form_data': request.POST,
                'teacher_id': teacher_id,
                'departments': departments,
                'designations': designations,
                'courses': courses
            })

        teacher = Teacher(
            teacher_id=teacher_id,
            username=username,
            last_name=last_name,
            email=email,
            department_id=department_id, 
            designation_id=designation_id
        )
        teacher.save()

        if selected_courses:
            teacher.courses.set(selected_courses)

        user = CustomUser(
            username=username,  
            email=email,
            full_name=f"{username} {last_name}",
            phone_number='',
            role='Teacher',
            teacher=teacher,
            is_super_admin=False
        )
        user.set_password(password)
        user.save()

        return redirect('teacher_list')

    # Handle GET request
    last_teacher = Teacher.objects.order_by('-created_on').first()
    teacher_id = 1 if last_teacher is None else int(last_teacher.teacher_id) + 1

    departments = Department.objects.all()
    designations = Designation.objects.all()
    courses = Courses.objects.all()

    return render(request, 'admin/teacher_account/add_tec_account.html', {
        'teacher_id': teacher_id,
        'departments': departments,
        'designations': designations,
        'courses': courses
    })



@login_required(login_url='home')
def teacher_list(request):  
    student = Teacher.objects.prefetch_related('courses').all()
    return render(request , 'admin/teacher_account/list_tec_account.html', { 'student':student })
def edit_teacher(request, teacher_id):
    student = get_object_or_404(Teacher, pk=teacher_id)

    if request.method == "POST":
        error_messages = {}
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        department_id = request.POST.get('department')
        designation_id = request.POST.get('designation')
        selected_courses = request.POST.getlist('courses')

        if not username:
            error_messages['username'] = "First Name is required."
        if not last_name:
            error_messages['last_name'] = "Last Name is required."
        if not email:
            error_messages['email'] = "Email is required."
       
        # if not password:
        #     error_messages['password'] = "Password is required."
        if not department_id:
            error_messages['department'] = "Department is required."

        if error_messages:
            departments = Department.objects.all()
            designations = Designation.objects.all()
            courses = Courses.objects.all()
            return render(request, 'admin/teacher_account/update_tec_account.html', {
                'error_messages': error_messages,
                'form_data': request.POST,
                'student': student,
                'departments': departments,
                'designations':designations,
                'courses': courses,
                'selected_courses': selected_courses
            })

        student.username = username
        student.last_name = last_name
        student.email = email
        student.password = password
        student.designation_id = designation_id
        student.department_id = department_id
        
        student.save()
        
        if selected_courses:
            student.courses.set(selected_courses)
        
        return redirect('teacher_list')

    departments = Department.objects.all()
    designations = Designation.objects.all()
    courses = Courses.objects.all()
    selected_courses = list(student.courses.values_list('id', flat=True))

    return render(request, 'admin/teacher_account/update_tec_account.html', {
        'student': student,
        'departments': departments,
        'designations': designations,
        'courses': courses,
        'selected_courses': selected_courses
    })


def get_courses(request):
    department_id = request.GET.get('department_id')
    courses = Courses.objects.filter(department_id=department_id).values('id', 'name')
    return JsonResponse({'courses': list(courses)})

# -----------------------------------------------------------------------------------------------------
# Designation
# -----------------------------------------------------------------------------------------------------

@login_required(login_url='home')
def designation_add(request):
    if request.method == "POST":
        last_designation = Designation.objects.order_by('-created_at').first()
        des_id = 1 if last_designation is None else int(last_designation.des_id) + 1

        name = request.POST.get('name')
        description = request.POST.get('description')
        error_messages = {}

        # Validation
        if not name:
            error_messages['name'] = "Name is required."
        
        if Designation.objects.filter(des_id=des_id).exists():
            error_messages['des_id'] = f"Designation ID '{des_id}' already exists."

        if error_messages:
            return render(request, 'admin/destination/designation_add.html', {
                'error_messages': error_messages,
                'form_data': request.POST
            })

        designation_add = Designation(
            des_id=des_id,
            name=name,
            description=description,
            created_at=timezone.now().date(),
        )
        designation_add.save()
        return redirect('designation_list')

    last_designation = Designation.objects.order_by('-created_at').first()
    des_id = 1 if last_designation is None else int(last_designation.des_id) + 1
    
    return render(request, 'admin/destination/designation_add.html', {"des_id": des_id})

@login_required(login_url='home')
def designation_list(request):  
    design = Designation.objects.all()
    context = {
        'design': design,
    }
    return render(request , 'admin/destination/designation_list.html',context)


@login_required(login_url='home')
def designation_update(request, designation_id):
    designation = get_object_or_404(Designation, pk=designation_id)
    if request.method == "POST":
        last_company = Designation.objects.order_by('-created_at').first()
        if last_company is None:
            des_id = 1
        
        name = request.POST['name']
        description = request.POST['description']
        error_messages = {}
        
        if not name:
            error_messages['name'] = "Name is required."
        # elif not name.isalpha():
        #     error_messages['name'] = "Name must contain only characters."       
        if error_messages:
            return render(request, 'admin/destination/designation_update.html', {
                'designation': designation,
                'error_messages': error_messages,
                'form_data': request.POST
            })

        designation.name = name
        designation.description = description
        designation.save()
        return redirect('designation_list')
    des_id = Designation.objects.order_by('-created_at').first()
    print(des_id)
    if des_id is None:
        des_id = 1
        print(des_id)
       
    context = {
        'designation': designation,
        "des_id":des_id
    }
    return render(request, 'admin/destination/designation_update.html', context)

@login_required(login_url='home')

def designation_delete(request,pk):
    designation = get_object_or_404(Designation, pk=pk)
    designation.delete()
    return redirect(designation_list)


#==============================Department==========================

@login_required(login_url='home')
def department_add(request):
    if request.method == "POST":
        last_department = Department.objects.order_by('-created_on').first()
        if last_department is None:
            dep_id = 1
        else:
            dep_id = int(last_department.dep_id) + 1

        if Department.objects.filter(dep_id=dep_id).exists():
            error_messages['dep_id'] = f"Department ID '{dep_id}' already exists."
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        error_messages = {}
        
        if not name:
            error_messages['name'] = "Name is required."
        # elif not name.isalpha():
        #     error_messages['name'] = "Name must contain only characters."

        if error_messages:
            return render(request, 'admin/department/department_add.html', {
                'error_messages': error_messages,
                'form_data': request.POST,
                'dep_id': dep_id  
            }) 

        department_add = Department(
            dep_id=dep_id,
            name=name,
            description=description,
            created_on=timezone.now().date(),
        )
        department_add.save()
        return redirect('department_list')

    last_department = Department.objects.order_by('-created_on').first()
    if last_department is None:
        dep_id = 1
    else:
        dep_id = int(last_department.dep_id) + 1

    return render(request, 'admin/department/department_add.html', {
        "dep_id": dep_id
    })

@login_required(login_url='home')
def department_list(request):  
    design = Department.objects.all()
    context = {
        'design': design,
    }
    return render(request , 'admin/department/department_list.html',context)


@login_required(login_url='home')
def department_update(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == "POST":
        last_company = Department.objects.order_by('-created_on').first()
        if last_company is None:
            dep_id = 1
        
        name = request.POST['name']
        description = request.POST['description']
        error_messages = {}
        
        if not name:
            error_messages['name'] = "Name is required."
           
        if error_messages:
            return render(request, 'admin/department/department_update.html', {
                'department': department,
                'error_messages': error_messages,
                'form_data': request.POST
            })

        department.name = name
        department.description = description
        
        department.save()
        return redirect('department_list')
    dep_id = Department.objects.order_by('-created_on').first()
    print(dep_id)
    if dep_id is None:
        dep_id = 1
        print(dep_id)
       
    context = {
        'department': department,
        "dep_id":dep_id
    }
    return render(request, 'admin/department/department_update.html', context)


@login_required(login_url='home')
def department_delete(request,pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect(department_list)



#==============================Courses==========================

@login_required(login_url='home')
def courses_add(request):
    if request.method == "POST":
        last_course = Courses.objects.order_by('-created_on').first()
        if last_course is None:
            course_id = 1
        else:
            course_id = int(last_course.course_id) + 1

        error_messages = {}
        name = request.POST.get('name')
        description = request.POST.get('description')
        department_id = request.POST.get('department')

        if not name:
            error_messages['name'] = "Name is required."
        
        if not department_id:
            error_messages['department'] = "Department is required."

        if error_messages:
            departments = Department.objects.all()  
            return render(request, 'admin/courses/courses_add.html', {
                'error_messages': error_messages,
                'form_data': request.POST,
                'course_id': course_id,
                'departments': departments  
            }) 

        course_add = Courses(
            course_id=course_id,
            name=name,
            department_id=department_id, 
            created_on=timezone.now().date(),
        )
        course_add.save()
        return redirect('courses_list')

    
    last_course = Courses.objects.order_by('-created_on').first()
    if last_course is None:
        course_id = 1
    else:
        course_id = int(last_course.course_id) + 1

    departments = Department.objects.all()  
    return render(request, 'admin/courses/courses_add.html', {
        "course_id": course_id,
        'departments': departments  
    })

@login_required(login_url='home')
def courses_list(request):  
    design = Courses.objects.all()
    context = {
        'design': design,
    }
    
    return render(request , 'admin/courses/courses_list.html',context)


@login_required(login_url='home')
def courses_update(request, courses_id):
    course = get_object_or_404(Courses, pk=courses_id)
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        department_id = request.POST.get('department')
        error_messages = {}

        if not name:
            error_messages['name'] = "Name is required."
        
        if not department_id:
            error_messages['department'] = "Department is required."

        if error_messages:
            departments = Department.objects.all()
            return render(request, 'admin/courses/courses_update.html', {
                'course': course,
                'error_messages': error_messages,
                'form_data': request.POST,
                'departments': departments
            })

       
        course.name = name
        course.description = description
        course.department_id = department_id
        course.updated_on = timezone.now().date()
        course.save()
        return redirect('courses_list')

    # For GET request
    departments = Department.objects.all()
    return render(request, 'admin/courses/courses_update.html', {
        'course': course,
        'departments': departments
    })


#==============================class==========================

@login_required(login_url='home')
def classes_add(request):
    if request.method == "POST":
        last_classes = Classes.objects.order_by('-created_on').first()
        if last_classes is None:
            classes_id = 1
        else:
            classes_id = int(last_classes.classes_id) + 1

        error_messages = {}
        name = request.POST.get('name')
        course_id = request.POST.get('course')

        if not name:
            error_messages['name'] = "Name is required."
        
        if not course_id:
            error_messages['course'] = "Course is required."

        if error_messages:
            courses = Courses.objects.all() 
            return render(request, 'admin/class/classes_add.html', {
                'error_messages': error_messages,
                'form_data': request.POST,
                'classes_id': classes_id,
                'courses': courses 
            }) 
  
        selected_course = Courses.objects.get(pk=course_id)  
        classes_add = Classes(
            classes_id=classes_id,
            name=name,
            courses=selected_course, 
            created_on=timezone.now(),
        )
        classes_add.save()
        return redirect('classes_list')

    last_classes = Classes.objects.order_by('-created_on').first()
    if last_classes is None:
        classes_id = 1
    else:
        classes_id = int(last_classes.classes_id) + 1

    courses = Courses.objects.all() 
    return render(request, 'admin/class/classes_add.html', {
        "classes_id": classes_id,
        'courses': courses  
    })

@login_required(login_url='home')
def classes_list(request):  
    classes = Classes.objects.all()
    context = {
        'classes': classes,
    }
    
    return render(request , 'admin/class/classes_list.html',context)

@login_required(login_url='home')
def classes_update(request, class_id):
    classes = get_object_or_404(Classes, pk=class_id)

    if request.method == "POST":
        error_messages = {}
        name = request.POST.get('name')
        course_id = request.POST.get('course')

        if not name:
            error_messages['name'] = "Name is required."

        if not course_id:
            error_messages['course'] = "Course selection is required."

        if error_messages:
            courses = Courses.objects.all()
            return render(request, 'admin/class/classes_update.html', {
                'error_messages': error_messages,
                'form_data': request.POST,
                'classes': classes,
                'courses': courses,
            })
       
        classes.name = name
        classes.courses_id = course_id
        classes.updated_on = timezone.now().date()
        classes.save()

        return redirect('classes_list')

    # For GET request
    courses = Courses.objects.all()
    return render(request, 'admin/class/classes_update.html', {
        'classes': classes,
        'courses': courses
    })

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%d-%m-%Y').date()  
    except ValueError:
        return None
# myapp/views.py
from django.shortcuts import render
from django.utils.dateparse import parse_date
# from .tasks import process_attendance_file
# from .google_drive import upload_file_to_google_drive  # Import the Google Drive function
# from .models import Attendance, Department, Courses, Classes, Student, Teacher
from .google_drive import *
# attendance/views.py
from django.shortcuts import render
# from .tasks import process_attendance_file
import os
# from .models import Attendance
from django.conf import settings

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str, format='%d-%m-%Y').date()
    except ValueError:
        return None
# attendance/views.py

def upload_and_filter_attendance(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')

        if uploaded_file:
            # Create the directory for attendance records if it doesn't exist
            attendance_dir = os.path.join(settings.MEDIA_ROOT, 'attendance_records')
            os.makedirs(attendance_dir, exist_ok=True)

            # Save the uploaded file temporarily and get the file path
            file_path = os.path.join(attendance_dir, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Call the upload_task with the required parameters
            # Note: We don't wait for Celery to finish, just queue the task
            upload_task.delay(file_path, from_date_str, to_date_str)

            # Return success message as a JSON response
            return JsonResponse({
                'message': 'File uploaded successfully. Processing in background. The page will reload shortly.',
                'success': True
            })

    # If not a POST request, just retrieve attendance records
    attendance_records = Attendance.objects.all().order_by('-to_date')

    return render(request, 'admin/attendance/filter_attendance.html', {
        'attendance_records': attendance_records
    })







@login_required
def view_attendance(request):
    from_date_str = request.GET.get('from_date')  
    to_date_str = request.GET.get('to_date')      
    class_id = request.GET.get('class')           
    attendance_status = request.GET.get('status')
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date() if from_date_str else None
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date() if to_date_str else None

    teacher = Teacher.objects.get(username=request.user.username)

    teacher_courses = teacher.courses.all()
    teacher_classes = Classes.objects.filter(courses__in=teacher_courses)

    attendance_records = Attendance.objects.filter(class_room__in=teacher_classes)

    if from_date:
        attendance_records = attendance_records.filter(date__gte=from_date)
    if to_date:
        attendance_records = attendance_records.filter(date__lte=to_date)
    if class_id:
        attendance_records = attendance_records.filter(class_room_id=class_id)
    if attendance_status:
        attendance_records = attendance_records.filter(status=attendance_status)

    today = now().date()

    return render(request, 'teacher/teacher_module/view_attendance.html', {
        'attendance_records': attendance_records,  
        'from_date': from_date_str,
        'to_date': to_date_str,
        'today': today,
        'classes': teacher_classes, 
        'selected_class': class_id,  
        'attendance_status': attendance_status  
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Teacher

@login_required(login_url='home')
def view_profile(request):  
    custom_user = request.user
    teacher = custom_user.teacher  
    teacher = Teacher.objects.prefetch_related('courses').get(id=teacher.id)
    
    return render(request, 'teacher/teacher_module/profile.html', {'teacher': teacher})

User = get_user_model()
from django.shortcuts import render

def view_courses(request):
    teacher = request.user.teacher  
    courses = Courses.objects.filter(id__in=teacher.courses.values_list('id', flat=True)).prefetch_related('teacher_set')
    
    context = {
        'courses': courses,
    }
    return render(request, 'teacher/teacher_module/view_courses.html', context)
