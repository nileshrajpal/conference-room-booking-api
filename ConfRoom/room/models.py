from django.db import models

from user.models import User


class Room(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=255, unique=True)
    desc = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Slot(models.Model):
    objects = models.Manager()

    room = models.ForeignKey(Room, related_name='slots', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    booked_by = models.ForeignKey(User, related_name='booked_slots',
                                  null=True, on_delete=models.SET_NULL)
