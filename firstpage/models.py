from django.db import models

# Create your models here.
class Product(models.Model):

    id = models.BigAutoField(primary_key=True) # each item has distinct id. gives each item unique number
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True) # can be left blank
    price = models.DecimalField(decimal_places = 2, max_digits=1000)
    image = models.ImageField(null=True, blank=True) # image has url
    listing_id	= models.IntegerField(blank=True, null=True)
    productLink = models.URLField(max_length=200)

    def imageURL(self):
        try:
            url = self.image.url
        except:
             url = ''

        return url
