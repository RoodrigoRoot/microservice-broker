from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.serializers import UserSerializer
from producer import RabbitMQBroker
# Create your views here.


class CreateGetUsersAPIView(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        RabbitMQBroker().publish(serializer.data)
        return Response({"ok": "ok"})
