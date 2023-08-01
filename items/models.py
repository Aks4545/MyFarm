from django.db import models
from seller.models import seller

# Create your models here.



class category(models.Model):
    vendor = models.ForeignKey(seller, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def clean(self):
        self.category_name = self.category_name.capitalize()
    
    def __str__(self):
        return self.category_name


class product(models.Model):
    vendor = models.ForeignKey(seller, on_delete=models.CASCADE)
    category= models.ForeignKey(category,on_delete=models.CASCADE,related_name='product')
    product_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='prod_image')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_title




