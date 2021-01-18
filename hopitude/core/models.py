from django.db import models


class IotDeviceData(models.Model):
    data_id = models.IntegerField(unique=True, editable=False)
    timestamp = models.PositiveBigIntegerField()
    status = models.CharField(max_length=50)
    rotor_speed = models.PositiveSmallIntegerField()
    slack = models.FloatField()
    root_threshold = models.FloatField()
    asset_id = models.IntegerField()
    asset_alias = models.CharField(max_length=150)
    parent_id = models.IntegerField(blank=True, null=True)
    parent_alias = models.CharField(max_length=150, blank=True, null=True)
