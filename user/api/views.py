import jwt

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.serializers import jwt_payload_handler

from user.api.serializers import RegistrationSerializer
from user.api.serializers import ResetPasswordSerializer
from ..models import User as UserModel


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = dict()
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully registered a new user"
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)


@api_view(['PATCH'])
def reset_password_view(request, user_id):
    user = UserModel.objects.get(id=user_id)
    serializer = ResetPasswordSerializer(user, data=request.data)
    data = dict()
    if serializer.is_valid():
        user = serializer.update(user, serializer.validated_data)
        data['response'] = "Successfully updated the password"
        data['username'] = user.username
    else:
        data = serializer.errors
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = UserModel.objects.get(username=username)
        if not user.check_password(password):
            return Response({'error': 'incorrect password'})
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details =  dict()
                user_details['username'] = user.username
                user_details['email'] = user.email
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'failed to authenticate with given credentials'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        return Response({'error': 'Please provide the username and password'})
