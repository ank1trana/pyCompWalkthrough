from django.db import models

#inherit Model by Proucts - allows things like store in a db, read, delete from db on moel objs
class Product(models.Model):
    name = models.CharField(max_length = 255)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)

class Offer(models.Model):
    code = models.CharField(max_length = 10)
    description = models.CharField(max_length = 255)
    discount = models.FloatField()
    
