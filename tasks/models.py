from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):

    PRIORITY_CHOICES =[
        ('L' , 'Low'),
        ('M' , 'Medium'),
        ('H' , 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='L')
    description = models.TextField()
    done = models.BooleanField(default=False)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    complete_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.task_name

    class Meta:
        ordering = ['-created_at']
        order_with_respect_to = 'user'
