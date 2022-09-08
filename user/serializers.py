from rest_framework import serializers

from django.contrib.auth import authenticate

from .models import User

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data["username"],password=validated_data["password"])

    class Meta:
        model = User
        fields = ["id","username","password","type_user"]
        extra_kwargs = {
            'password': {'required': True, 'write_only': True}
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        return {'user': user}
