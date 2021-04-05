from django.db import models
from django.utils import timezone

# Create your models here.
class Ads(models.Model):
    company_name = models.CharField(max_length=50) # Company Name
    image = models.ImageField( upload_to='ad_images/',blank = True, null= True) # Adding multiple image according to device??

    # Header, Content, Sidebar
    AD_CHOICES = (
        ('H','header'),
        ('C','content'),
        ('S','sidebar'),
    )

    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)

    ad_position = models.CharField(max_length=2, choices= AD_CHOICES, default='H')

    # profile_pic_status = models.BooleanField(default=True)
    # use duration field to decide which ad gets placed

    duration_start = models.DateTimeField(default=timezone.now)
    duration_end = models.DateTimeField(default=timezone.now)
    clicks = models.IntegerField(default = 0)
    url = models.URLField(max_length=200)


    # Add display status boolean data type to represent whether that image is the profile pic

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        return f"ad/showad/"

    
    