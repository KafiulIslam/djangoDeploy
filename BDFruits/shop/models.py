from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Fruit(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.CharField(max_length=500)
    fruit_image = models.ImageField(upload_to='fruit-img')

    def __str__(self):
        return self.title

    @property
    def discount_percent(self):
        if self.selling_price and self.discounted_price < self.selling_price:
            return round(
                (self.selling_price - self.discounted_price) * 100 / self.selling_price
            )
        return 0


# Division choices
DIVISION_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Rangpur', 'Rangpur'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barisal', 'Barisal'),
    ('Chattagram', 'Chattagram'),
    ('Mymenshing', 'Mymenshing'),
    ('Sylhet', 'Sylhet'),
)

# Address Type choices
ADDRESS_TYPE_CHOICES = (
    ('Home', 'Home'),
    ('Office', 'Office'),
    ('Apartment', 'Apartment')
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    division = models.CharField(choices=DIVISION_CHOICES, max_length=50)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=200)
    villorroad = models.CharField(max_length=100)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.name


class CustomerAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    division = models.CharField(choices=DIVISION_CHOICES, max_length=50)
    district = models.CharField(max_length=200)
    thana = models.CharField(max_length=200)
    roadNumber = models.CharField(max_length=500)
    zipCode = models.IntegerField()
    addressType = models.CharField(choices=ADDRESS_TYPE_CHOICES, max_length=20)

    def __str__(self):
        return self.district