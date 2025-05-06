from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer  


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

@api_view(['POST', 'GET'])
def task_search(request):
    if request.method == 'POST':
        data = request.data
    else:  
        data = request.GET

    search = data.get('search', '')
    is_done = data.get('is_done', None)

    tasks = Task.objects.all()
    if search:
        tasks = tasks.filter(title__icontains=search)
    if is_done is not None:
        tasks = tasks.filter(is_done=is_done)

    paginator = PageNumberPagination()
    paginator.page_size = 7  
    result_page = paginator.paginate_queryset(tasks, request)

    serializer = TaskSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
