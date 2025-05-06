from rest_framework.routers import DefaultRouter
from django.urls import path, include
from tasks.views import TaskViewSet, task_search
from rest_framework_simplejwt import views as jwt_views
from tasks import views  
from rest_framework_simplejwt.views import TokenRefreshView
from tasks.views import TokenRefreshViewCustom

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/tasks/search/', task_search),  
    path('api/', include(router.urls)),  
    
   
    path('api/signup/', views.signup, name='signup'),            
    path('api/login/', views.login, name='login'),               
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  
    path('api/token/refresh/', TokenRefreshViewCustom.as_view(), name='token_refresh'),
]



  
