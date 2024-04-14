from django.db import models
from django.utils import timezone


class Book(models.Model):
    book_id = models.CharField(max_length=20, unique=True, primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    issuedBy = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    registration_no = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.IntegerField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + self.last_name


class Log(models.Model):
    book_id = models.IntegerField()
    issued_by = models.CharField(max_length=100)
    issue_date_time = models.DateTimeField(default=timezone.now)
    return_date_time = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField()
    return_status = models.BooleanField(default=False)  # True if returned, False otherwise
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

