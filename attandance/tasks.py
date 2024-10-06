# attandance/tasks.py

from celery import shared_task
import pandas as pd
from .models import Attendance, Department, Courses, Classes, Student, Teacher
from django.utils.dateparse import parse_date
import os
import pandas as pd
from datetime import datetime

def parse_date(date_str):
    """Parse a date string in the format 'dd-mm-yyyy'."""
    try:
        return pd.to_datetime(date_str, format='%d-%m-%Y').date()
    except ValueError:
        return None

@shared_task()
def upload_task(from_date_str=None, to_date_str=None):
    file_path = r'D:/project/attandance_pro/attendance-record/attendance-record/ICT.xlsx'
    
    print("Upload task is running!")

    # Define your date range here if needed
    from_date = parse_date(from_date_str) if from_date_str else None
    to_date = parse_date(to_date_str) if to_date_str else None

    if not os.path.exists(file_path):
        return f"File not found at: {file_path}"

    try:
        # Load Excel file
        data = pd.read_excel(file_path)
        data.columns = data.columns.str.strip()
        
        # Rename columns to match your data
        data.rename(columns={
            'course': 'Course',
            'Departme': 'Department',
            'Class room:': 'Class',
            'Status:': 'Status',
            'to_date': 'To Date',
            'from_date': 'From Date',
            'username': 'First Name',
            'last_name': 'Last Name',
            'teacher_username': 'Teacher First Name',
            'teacher_last_name': 'Teacher Last Name'
        }, inplace=True)

        # Fetch required data for mapping
        departments = {d.name.lower(): d for d in Department.objects.all()}
        courses = {f"{c.name.lower()}-{c.department.name.lower()}": c for c in Courses.objects.select_related('department').all()}
        classes = {f"{cl.name.lower()}-{cl.courses.name.lower()}": cl for cl in Classes.objects.select_related('courses').all()}
        students = {f"{s.username.strip().lower()} {s.last_name.strip().lower()}": s for s in Student.objects.all()}
        teachers = {f"{t.username.strip().lower()} {t.last_name.strip().lower()}": t for t in Teacher.objects.all()}

        # Process each row
        for index, row in data.iterrows():
            # Debugging: print the current row
            print(f"Processing row {index}: {row.to_dict()}")

            # Date parsing and filtering
            record_to_date = parse_date(row.get('To Date'))
            record_from_date = parse_date(row.get('From Date'))

            # Debugging: check parsed dates
            print(f"Parsed dates - From: {record_from_date}, To: {record_to_date}")

            if record_to_date and record_from_date:
                if from_date and record_to_date < from_date:
                    continue
                if to_date and record_from_date > to_date:
                    continue

            # Fetch matching student, teacher, department, etc.
            student_key = f"{row.get('First Name', '').strip().lower()} {row.get('Last Name', '').strip().lower()}"
            student = students.get(student_key)

            if not student:
                continue

            teacher_key = f"{row.get('Teacher First Name', '').strip().lower()} {row.get('Teacher Last Name', '').strip().lower()}"
            teacher = teachers.get(teacher_key)

            department = departments.get(row.get('Department', '').strip().lower())
            if not department:
                continue

            course_key = f"{row.get('Course', '').strip().lower()}-{department.name.lower()}"
            course = courses.get(course_key)
            if not course:
                continue

            class_key = f"{row.get('Class', '').strip().lower()}-{row.get('Course', '').strip().lower()}"
            class_room = classes.get(class_key)
            if not class_room:
                continue

            # Create Attendance record
            Attendance.objects.create(
                to_date=record_to_date,
                from_date=record_from_date,
                department=department,
                course=course,
                student=student,
                teacher=teacher,
                class_room=class_room,
                status=row['Status']
            )

        return 'Attendance file processed successfully.'

    except Exception as e:
        return f'Error processing file: {str(e)}'
