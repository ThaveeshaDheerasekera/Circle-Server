from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AuthSerializer
import jwt
import datetime
import logging

logger = logging.getLogger(__name__)


class RegisterUser(APIView):
    @staticmethod
    def post(request):
        try:
            serializer = AuthSerializer(data=request.data)
            if serializer.is_valid():
                # Check if the username and email are unique
                username = serializer.validated_data['username']
                email = serializer.validated_data['email']
                if User.objects.filter(username=username).exists():
                    error_message = f'Username [ {username} ] is already taken'
                    return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
                if User.objects.filter(email=email).exists():
                    error_message = f'Email address [ {email} ] is already registered'
                    return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
                user = AuthSerializer(User.objects.create_user(**serializer.validated_data))
                # Return a success message or user data
                return Response({'message': user.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = str(e)
            logger.exception('Error in registerUser method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginUser(APIView):
    @staticmethod
    def post(request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = User.objects.filter(username=username).first()

            if user is None:
                error_message = f'User with username [ {username} ] not found'
                return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

            if not user.check_password(password):
                error_message = f'Incorrect Password'
                return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)

            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response({'token': token}, status=status.HTTP_200_OK)
            # response.set_cookie(key='token', value=token, httponly=True)
            return response
        except Exception as e:
            error_message = str(e)
            logger.exception('Error in loginUser method')
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
