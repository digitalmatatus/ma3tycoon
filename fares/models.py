from django.db import models

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Fare(models.Model):
    """A new fare entry

    """
    stop_to = models.CharField(
        max_length=255, blank=True, null=True,)
    stop_from = models.CharField(
        max_length=255, blank=True, null=True,)
    amount = models.CharField(
        max_length=255, blank=True, null=True,)
    stop_from_id = models.CharField(
        max_length=255, blank=True, null=True,)
    route_id = models.CharField(
        max_length=255, blank=True, null=True,)
    stop_to_id = models.CharField(
        max_length=255, blank=True, null=True,)
    weather = models.CharField(
        max_length=255, blank=True, null=True,)
    traffic_jam = models.CharField(
        max_length=255, blank=True, null=True,)
    demand = models.CharField(
        max_length=255, blank=True, null=True,)
    air_quality = models.CharField(
        max_length=255, blank=True, null=True,)
    peak = models.CharField(
        max_length=255, blank=True, null=True,)
    travel_time = models.CharField(
        max_length=255, blank=True, null=True,)
    crowd = models.CharField(
        max_length=255, blank=True, null=True,)
    safety = models.CharField(
        max_length=255, blank=True, null=True,)
    drive_safety = models.CharField(
        max_length=255, blank=True, null=True,)
    music = models.CharField(
        max_length=255, blank=True, null=True,)
    internet = models.CharField(
        max_length=255, blank=True, null=True,)
    date_added = models.DateTimeField(default=timezone.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "%s %s %s" % (self.stop_to, self.stop_from, self.amount)
