from rest_framework import serializers

from .models import User
from room.serializers import SlotSerializer


class UserSerializer(serializers.ModelSerializer):
    booked_slots = SlotSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email',
                  'bio', 'is_admin', 'booked_slots']


class UserSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email',
                  'bio', 'is_admin']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super(UserSettingsSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserSettingsSerializer, self).update(instance, validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]
