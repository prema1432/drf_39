from django.db import models


# Create your models here.


class School(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=560)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField()
    city = models.CharField(max_length=100)
    # school = models.ForeignKey(School, on_delete=models.CASCADE) # when u delte the school name will also be deleted
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True,
                               blank=True)  # when u delte the school name will also be deleted

    def __str__(self):
        return self.name
