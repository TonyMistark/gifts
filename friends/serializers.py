from rest_framework import serializers as sl


class CreateUserSerializer(sl.Serializer):
    username = sl.CharField(min_length=3, max_length=20)
    phone = sl.CharField(min_length=11, max_length=11, required=False)