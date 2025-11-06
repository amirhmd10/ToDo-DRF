from rest_framework import serializers
from .models import Task
from datetime import date

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_name', 'description', 'done', 'date']
        read_only_fields = ('created_at','user' ,)


    def validate_date (self, value):
        if value < date.today():
            raise serializers.ValidationError('Date must be in the future')
        return value
