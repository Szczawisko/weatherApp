from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from .menager import UserMenager

from .models import User

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
            UserMenager.save_user(data)
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

        serialaizer = UserSerializer(instance=user,data=data,partial=True)
        if serialaizer.is_valid():
            serialaizer.save()
            return Response(serialaizer.data, status=status.HTTP_201_CREATED)

        return Response(serialaizer.errors,status=status.HTTP_400_BAD_REQUEST)

        