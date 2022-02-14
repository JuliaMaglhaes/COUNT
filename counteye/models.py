from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.models import NewUser

def upload_to(instance, filename):
    return 'count/{filename}'.format(filename=filename)

#categoria dos produtos
class Category(models.Model):
    name = models.CharField(max_length=110)

    def __str__(self):
        return self.name

#Contagem
class Count(models.Model):

    class CountObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='counted')
    
    options = ('counted', 'Counted'),

    category = models.ForeignKey(Category, on_delete = models.PROTECT, default = 1)
    product = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(_("Image"), upload_to = upload_to, default='count/default.jpg')
    amount = models.IntegerField(blank=True, null=True)
    # slug = models.SlugField(max_length=250, unique_for_date = 'counted')
    counted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(NewUser, on_delete = models.CASCADE, related_name = 'user', blank=True, null=True)
    status = models.CharField(max_length=10, choices = options, default='counted')
    objects = models.Manager()
    postobjects = CountObjects()

    class Ordering:
        ordering = ('-counted',)
    

def upload(instance, filename):
    return 'conf/p/{filename}'.format(filename=filename)

class ProductsRegister(models.Model):
    category = models.ForeignKey(Category, on_delete = models.PROTECT, default = 1)
    product = models.CharField(max_length=250, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.product
