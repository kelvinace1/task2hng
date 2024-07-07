from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': serializer.data
                }
            }, status=status.HTTP_201_CREATED)
        else:
            errors = []
            for field, messages in serializer.errors.items():
                for message in messages:
                    errors.append({
                        'field': field,
                        'message': message
                    })
            return Response({
                'status': 'Bad request',
                'message': 'Registration unsuccessful',
                'status_code': status.HTTP_400_BAD_REQUEST,
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            serializer = UserSerializer(user)
            refresh = RefreshToken.for_user(user)

            return Response({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': serializer.data
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Bad request',
                'message': 'Authentication failed',
                'status_Code':  status.HTTP_401_UNAUTHORIZED,
                'errors': [
                    {
                        'field': 'email',
                        'message': 'Invalid email or password.'
                    }
                ]
            }, status=status.HTTP_401_UNAUTHORIZED) 