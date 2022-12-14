from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions

from .serializers import UserSerializer, LoginSerializer
from .menager import UserMenager
from .JWTAuthentication import JWTMenager


class UserListApiView(APIView):

    def get(self,request,*args, **kwargs):
        users = UserMenager.get_all_users()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        data = {
            "username":request.data.get("username"),
            "password":request.data.get("password"),
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"res":"User was created"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPermissions(APIView):
    def put(self,request,id,*args, **kwargs):
        user = UserMenager.get_user(id)
        if not user:
            return Response({"res": "Object with entrie id does not exist"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "username":user.username,
            "type_user":request.data.get("permissions")
        }

        serializer = UserSerializer(instance=user,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):

    def post(self,request,*args, **kwargs):
        data = {
            "username":request.data.get("username"),
            "password":request.data.get("password"),
        }
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            menager = JWTMenager()
            tokens = menager.login(serializer.validated_data['user'])
            return Response(tokens,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_401_UNAUTHORIZED)

class TokenRefresh(APIView):

    def post(self,request,*args, **kwargs):
        token = request.data.get("refresh")
        menager = JWTMenager()
        try:
            refresh_token = menager.create_new_token(token)
            return Response(refresh_token,status=status.HTTP_200_OK)
        except exceptions.ParseError as e:
            return Response({"res":e.detail},status=status.HTTP_400_BAD_REQUEST)
        