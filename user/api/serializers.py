from rest_framework import serializers

from user.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'is_admin']

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        is_admin = self.validated_data['is_admin']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'password':'Passwords do not match'})
        user.set_password(password)
        if is_admin:
            user.is_admin = True
        user.save()
        return user


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password']

    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)

    def update(self, instance, validated_data):
        # check if the old password is correct
        if not instance.check_password(self.validated_data['old_password']):
            raise serializers.ValidationError({'Password': 'Old password is incorrect, try again!'})
        password = self.validated_data['new_password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        instance.set_password(password)
        instance.save()
        print(instance.username)
        return instance
