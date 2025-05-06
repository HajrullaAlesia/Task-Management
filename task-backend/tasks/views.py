from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from .models import Task
from .serializers import TaskSerializer, UserSerializer  
from rest_framework_simplejwt.views import TokenRefreshView


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer




class TokenRefreshViewCustom(TokenRefreshView):
    pass


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  

            
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            
            return Response({
                'refresh': str(refresh),
                'access': str(access_token)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')  
    password = request.data.get('password')

    try:
        
        user = User.objects.get(email=email)  
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

           
            return Response({
                'refresh': str(refresh),
                'access': str(access_token)
            })

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


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
