from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserSerializer  


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        access_token = AccessToken.for_user(user)

        return Response({'access': str(access_token)}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')  
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            access_token = AccessToken.for_user(user)

            return Response({'access': str(access_token)})

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
