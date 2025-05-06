from rest_framework.routers import DefaultRouter
from django.urls import path, include
from tasks.views import TaskViewSet, task_search
from users import views


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/tasks/search/', task_search),  
    path('api/', include(router.urls)),  
    path('api/signup/', views.signup, name='signup'),            
    path('api/login/', views.login, name='login'),               
]


