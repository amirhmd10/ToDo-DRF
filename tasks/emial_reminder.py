from django.contrib.auth import user_logged_in
from django.core.mail import send_mail
from django.contrib.auth.models import User
from datetime import date
from .models import Task

def send_daily_notification():
    today = date.today()
    user = User.objects.all()

    for user in user:
        tasks = Task.objects.filter(user=user , date=today , done=False)

        if tasks.exists() and user.email:
            subject = f'work list of {today}'
            task_list = "\n".join([f"- {task.task_name}" for task in tasks])
            message = f'hi {user.username}!\n\n{task_list} not completed.'

            send_mail(subject, message, from_email=None, recipient_list=[user.email] , fail_silently=False)


