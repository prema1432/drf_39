from django.contrib.auth.models import User
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


OFFER_TYPE = (
    ('FLAT', 'FLAT'),
    ('PERCENTAGE', 'PERCENTAGE'),
)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE)
    offer_amount = models.IntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
