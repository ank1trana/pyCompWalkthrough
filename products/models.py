from django.db import models

#inherit Model by Proucts - allows things like store in a db, read, delete from db on moel objs
class Product(models.Model):
    name = models.CharField(max_length = 255)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)


    
