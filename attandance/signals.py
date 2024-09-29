# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from django.utils.timezone import now
# from .models import Attendance, Classes

# @receiver(user_logged_in)

# def update_attendance_on_login(sender, user, request, **kwargs):
#     try:
#         student = user.student
#         today = now().date()
#         class_room_id = request.GET.get('class_room_id')  # Or get it from a form

#         # Check if the class_room_id is valid
#         if not class_room_id:
#             raise ValueError("Class Room ID is required")

#         class_room = Classes.objects.get(pk=class_room_id)  # Fetch the class room instance

#         attendance_record, created = Attendance.objects.get_or_create(
#             student=student,
#             date=today,
#             defaults={
#                 'status': 'Present',
#                 'entry_time': now(),
#                 'class_room': class_room
#             }
#         )

#         if not created:
#             # If the record exists, update the entry_time
#             attendance_record.entry_time = now()
#             attendance_record.save()
#     except (AttributeError, ValueError, Classes.DoesNotExist) as e:
#         # Handle errors
#         print(e)
#         pass
