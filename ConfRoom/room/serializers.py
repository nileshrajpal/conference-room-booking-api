from rest_framework import serializers

from user.models import User
from .models import Room, Slot


class UserInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ["id", "username"]


class RoomSlotSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(default=True)
    booked_by = UserInfoSerializer(read_only=True)

    class Meta:
        model = Slot
        fields = ['id', 'start_time', 'end_time', 'is_available', 'booked_by']


class RoomSerializer(serializers.ModelSerializer):
    slots = RoomSlotSerializer(many=True, required=False)

    class Meta:
        model = Room
        fields = ['id', 'name', 'desc', 'slots']

    def create(self, validated_data):
        if 'slots' in validated_data:
            slots = validated_data.pop('slots')
            room = Room.objects.create(**validated_data)
            for slot in slots:
                Slot.objects.create(room=room, **slot)
            return room
        else:
            room = Room.objects.create(**validated_data)
            return room


class SlotRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'desc']


class SlotSerializer(serializers.ModelSerializer):
    room = SlotRoomSerializer(read_only=True)
    is_available = serializers.BooleanField(default=True)
    booked_by = UserInfoSerializer(read_only=True)

    class Meta:
        model = Slot
        fields = ['id', 'room', 'start_time', 'end_time', 'is_available', 'booked_by']
