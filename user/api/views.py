from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.api.serializers import RegistrationSerializer
from user.api.serializers import ResetPasswordSerializer
from ..models import User as UserModel

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
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
    data = {}
    if serializer.is_valid():
        user = serializer.update(user, serializer.validated_data)
        data['response'] = "Successfully updated the password"
        data['username'] = user.username
    else:
        data = serializer.errors
    return Response(data)

'''
{
 "email" : "asjad@asjad.com",
 "username": "asjad18",
 "password": "abcabc",
 "confirm_password": "abcabc",
 "is_admin": false
}
'''