from django.db import models
from datetime import datetime

# Create your models here.


class Station(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Department(models.Model):
    dep_name = models.CharField(max_length=50)

    def __str__(self):
        return self.dep_name


class Status(models.Model):
    class Meta:
        verbose_name_plural = "Status"

    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status


class FaultDetail(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    fault_no = models.IntegerField()
    fault_description = models.TextField()
    fault_date = models.CharField(max_length=20)
    current_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    rectification_date = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True)
    user_id = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
