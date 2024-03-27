import datetime
from django.db import models
from ..login.models import User


class Route(models.Model):
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    route_datetime_create = models.DateTimeField(default=datetime.datetime.now)
    desirable_price = models.FloatField(blank=True, null=True)
    route_datetime = models.DateTimeField()

    dep_lng = models.FloatField(blank=True, null=True)
    dep_lat = models.FloatField(blank=True, null=True)

    dst_lng = models.FloatField(blank=True, null=True)
    dst_lat = models.FloatField(blank=True, null=True)


class RouteStatus(models.Model):
    fk_route = models.ForeignKey(Route, on_delete=models.CASCADE, db_column='fk_route')

    STATUS_CHOICES = (
        (1, 'active'),
        (0, 'inactive')
    )
    status = models.IntegerField(choices=STATUS_CHOICES)

    def __str__(self) -> str:
        return f'id{self.fk_route.id}: {self.get_status_display()}'


class Order(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="fk_user")
    fk_route_status = models.ForeignKey(RouteStatus, on_delete=models.CASCADE, db_column="fk_route_status")
    type_order = models.CharField(max_length=15, default="пешеход")
