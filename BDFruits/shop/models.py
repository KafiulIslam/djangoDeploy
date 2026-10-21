from django.db import models


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
