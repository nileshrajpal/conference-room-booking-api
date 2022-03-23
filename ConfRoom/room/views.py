from rest_framework.views import APIView
from rest_framework import status

from .models import Room, Slot

from .serializers import RoomSerializer, SlotSerializer, RoomSlotSerializer

from rest_framework import permissions
from room.permissions import IsAdminOrReadOnly, IsSlotOwner

from rest_framework.serializers import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework.response import Response

from datetime import datetime


class RoomView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated & IsAdminOrReadOnly]

    serializer_class = RoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query is not None:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Room list successfully retrieved",
                    "result": serializer.data}
        return Response(response)

    def create(self, request, *args, **kwargs):
        returned = super(RoomView, self).create(request, args, kwargs)
        # print(request.user.is_admin)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Room successfully created",
                    "result": returned.data}
        return Response(response)


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated & IsAdminOrReadOnly]

    queryset = Room.objects.all()
    lookup_url_kwarg = "room_id"
    serializer_class = RoomSerializer

    def retrieve(self, request, *args, **kwargs):
        super(RoomDetailView, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance)

        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Room successfully retrieved",
                    "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(RoomDetailView, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Room successfully updated",
                    "result": data}
        return Response(response)

    def delete(self, request, *args, **kwargs):
        super(RoomDetailView, self).delete(request, args, kwargs)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Room successfully deleted"}
        return Response(response)


class RoomSlotView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Slot.objects.filter(room__id=self.kwargs["room_id"])

        is_available = self.request.query_params.get('is_available', None)
        if is_available is not None:
            if is_available.lower() == 'true':
                queryset = queryset.filter(is_available=True)
            else:
                queryset = queryset.filter(is_available=False)
        return queryset

    lookup_url_kwarg = "room_id"
    serializer_class = SlotSerializer

    def perform_create(self, serializer):
        is_valid = True
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        slots = Slot.objects.filter(room__id=self.kwargs["room_id"])
        for slot in slots:
            # print(slot.start_time, slot.end_time)
            if start_time >= slot.end_time or end_time <= slot.start_time:
                pass
            else:
                is_valid = False
                break

        if not is_valid:
            raise ValidationError({'message': "Time slot overlap, expecting unique time slot"},
                                  code=status.HTTP_400_BAD_REQUEST)

        if start_time > end_time:
            raise ValidationError({'message': "Start time can't be later than end time"
                                              "(Time slot should be entirely of today only)"},
                                  code=status.HTTP_400_BAD_REQUEST)

        s_time = datetime.strptime(str(start_time), "%H:%M:%S")
        e_time = datetime.strptime(str(end_time), "%H:%M:%S")
        time_dif = e_time - s_time
        if time_dif.total_seconds() > 3600:
            raise ValidationError({'message': "Slot duration can't be more than 1 hour (3600 seconds)"},
                                  code=status.HTTP_400_BAD_REQUEST)

        if time_dif.total_seconds() < 600:
            raise ValidationError({'message': "Slot duration can't be less than 10 minutes (600 seconds)"},
                                  code=status.HTTP_400_BAD_REQUEST)

        serializer.save(room=Room.objects.get(id=self.kwargs["room_id"]))

    def list(self, request, **kwargs):
        try:
            room = Room.objects.get(id=self.kwargs["room_id"])
            queryset = self.get_queryset()
            slot_serializer = RoomSlotSerializer(queryset, many=True)
            results = {
                "id": room.id,
                "name": room.name,
                "desc": room.desc,
                "slots": slot_serializer.data
            }
            response = {"status_code": status.HTTP_200_OK,
                        "message": "Slot list successfully retrieved",
                        "results": results}
            return Response(response)
        except ObjectDoesNotExist:
            response = {"status_code": status.HTTP_404_NOT_FOUND,
                        "message": "Room doesn't exist"}
            return Response(response)

    def create(self, request, *args, **kwargs):
        returned = super(RoomSlotView, self).create(request, args, kwargs)
        # print(request.user.is_admin)
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Slot successfully created",
                    "result": returned.data}
        return Response(response)


class RoomSlotDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request, room_id, slot_id):
        try:
            slot = Slot.objects.get(id=slot_id, room__id=room_id)
        except ObjectDoesNotExist:
            response = {"status_code": status.HTTP_404_NOT_FOUND,
                        "message": "Slot/Room doesn't exist or slot doesn't belong to the room"}
            return Response(response)

        serializer = SlotSerializer(slot)
        data = serializer.data
        response = {"status_code": status.HTTP_200_OK,
                    "message": "Slot successfully retrieved",
                    "result": data}
        return Response(response)

    def delete(self, request, room_id, slot_id):
        try:
            slot = Slot.objects.get(id=slot_id, room__id=room_id)
            slot.delete()
            response = {"status_code": status.HTTP_200_OK,
                        "message": "Slot successfully deleted"}
            return Response(response)

        except ObjectDoesNotExist:
            response = {"status_code": status.HTTP_404_NOT_FOUND,
                        "message": "Slot/Room doesn't exist or slot doesn't belong to the room"}
            return Response(response)


class RoomSlotBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, room_id, slot_id):
        try:
            slot = Slot.objects.get(room__id=room_id, id=slot_id)
        except ObjectDoesNotExist:
            response = {"status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "Slot/Room doesn't exist or slot doesn't belong to the room"}
            return Response(response)

        if slot.is_available:
            is_valid = True
            user_slots = Slot.objects.filter(booked_by=request.user)
            for user_slot in user_slots:
                # print(user_slot.start_time, user_slot.end_time)
                if slot.start_time >= user_slot.end_time or slot.end_time <= user_slot.start_time:
                    pass
                else:
                    is_valid = False
                    break

            if not is_valid:
                response = {"status_code": status.HTTP_400_BAD_REQUEST,
                            "message": "This time slot overlaps with a time slot you've already booked"}
                return Response(response)

            if slot.start_time > datetime.now().time():
                slot.is_available = False
                slot.booked_by = request.user
                slot.save()
                response = {"status_code": status.HTTP_200_OK,
                            "message": "Slot booked successfully"}
                return Response(response)
            else:
                response = {"status_code": status.HTTP_400_BAD_REQUEST,
                            "message": "Can't book a slot whose time has already elapsed"}
                return Response(response)
        else:
            response = {"status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "Slot is already booked (isn't available)"}
            return Response(response)


class RoomSlotCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSlotOwner]

    def post(self, request, room_id, slot_id):
        try:
            slot = Slot.objects.get(room__id=room_id, id=slot_id)
        except ObjectDoesNotExist:
            response = {"status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "Room or Slot doesn't exist"}
            return Response(response)

        self.check_object_permissions(self.request, slot)

        if not slot.is_available:
            slot = Slot.objects.get(id=slot_id)
            slot.is_available = True
            slot.booked_by = None
            slot.save()
            response = {"status_code": status.HTTP_200_OK,
                        "message": "Slot booking cancelled successfully"}
            return Response(response)
        else:
            response = {"status_code": status.HTTP_400_BAD_REQUEST,
                        "message": "There is no slot booking to cancel"}
            return Response(response)
