from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date, timedelta
from .models import Task
from .serializers import TaskSerializer



class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-date')


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permissions_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)



class DailyProgressListView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request):
        user = request.user
        selected_date = request.query_params.get('date' ,None)

        if selected_date:
            try:
                selected_date = date.fromisoformat(selected_date)
            except ValueError:
                return Response({'Errore' : 'format not match'} , status=400)
        return Response({'date': selected_date.isoformat()})

        tasks = Task.objects.filter(user=user, date=selected_date)
        total = task.count()
        done = tasks.filter(done=True).count()

        progress = round ((done/total) * 100 , 2) if total > 0 else 0

        return Response({
            'date' : selcted_date ,
            'total' : total,
            'progress' : progress,
            'progressPercent' : progress
        })


class WeeklyProgressListView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request):
        user = request.user
        today = date.today()
        start_date = today - timedelta(days=today.weekday())
        end_date = today + timedelta(days=7)

        tasks = Task.objects.filter(date__gte=start_date,date__lte=end_date , user=user)

        grouped = (
            tasks.values(
                total = Count('id'),
                done = Count('id' , filter = Q(done=True))
            )
            .order_by('date')
        )
        results = []

        for g in grouped :
            total = g['total']
            done = g['done']
            progress = round((done/total) * 100 , 2) if total > 0 else 0
            results.append({
                'date': g['date'],
                'total_tasks': total,
                'done_tasks': done,
                'progress_percent': progress
            })

            # [
            #     {"date": "2025-11-03", "total_tasks": 5, "done_tasks": 2, "progress_percent": 40.0},
            #     {"date": "2025-11-04", "total_tasks": 4, "done_tasks": 3, "progress_percent": 75.0},
            #     {"date": "2025-11-05", "total_tasks": 6, "done_tasks": 5, "progress_percent": 83.33}
            # ]

        return Response(results)


