from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.utils import timezone

class Designation(models.Model):
    des_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=255, )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    dep_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=255, )
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
class Courses(models.Model):
    course_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=255, )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
class Classes(models.Model):
    classes_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=255)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Courses, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.username} {self.last_name}"

class Student(models.Model):
    student_id = models.CharField(max_length=50)
    username = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    # Foreign keys and many-to-many relationships
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    courses = models.ManyToManyField(Courses)
    # student_class = models.ForeignKey(Classes, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.username} {self.last_name} - {self.student_id}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    to_date = models.DateField(null=True)
    from_date = models.DateField(null=True)
    # date = models.DateField()
    date = models.DateField(null=True)
    # entry_time = models.DateTimeField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_room = models.ForeignKey(Classes, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.teacher}"


class UploadedFiles(models.Model):
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class FileWords(models.Model):
    word = models.CharField(max_length=255)
    file_id = models.ForeignKey(UploadedFiles, on_delete=models.CASCADE)

    def __str__(self):
        return self.word



# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

# CustomUser Model
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=50, null=True)
    date_of_creation = models.DateField(auto_now_add=True, null=True)
    last_login_date = models.DateField(blank=True, null=True)
    is_super_admin = models.BooleanField(default=False)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True, blank=True) 
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username

# AdminUser Model
class AdminUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return self.user.username

