from django.db import models
from django.contrib.auth.models import User


class trip(models.Model):
    trip_name=models.CharField(max_length=100)
    trip_completed=models.BooleanField(default=False)
    user=models.ManyToManyField(User)
    def __str__(self):
        return self.trip_name
class tasks(models.Model):
    trip_name1 = models.ForeignKey(trip,on_delete=models.CASCADE, db_index=True)
    task=models.CharField(max_length=100)
    whopaid=models.CharField(max_length=100)
    taskexp=models.IntegerField()
    def __str__(self):
        return self.task
class friend(models.Model):
    friends=models.CharField(max_length=100)
    user=models.ForeignKey(trip,on_delete=models.CASCADE)
    def __str__(self):
        return self.friends
