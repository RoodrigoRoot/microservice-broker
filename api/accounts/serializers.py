from rest_framework import serializers

class UserSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    last_name = serializers.CharField(max_length=50)
