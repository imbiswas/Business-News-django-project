from __future__ import unicode_literals
from django.db import models
from django.utils.text import slugify
from uuid import uuid4
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.title
    
    @property
    def get_products(self):
        return news.objects.filter(category__title=self.title)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
        
class news(models.Model):
    Heading = models.CharField(max_length=100)
    # News = models.TextField()
    News = RichTextUploadingField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    tags = models.CharField(max_length= 100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.CharField(max_length=32)
    excerpt = models.TextField()
    slug = models.SlugField(unique=True, default=uuid4)
    viewcount = models.IntegerField(default=0)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')

    # def __str__(self):
    #     return '%s'%(self.Heading)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.Heading)
    #     super(news, self).save(*args, **kwargs)

    class Meta:
      ordering = ["-timestamp"] 

class Images(models.Model):
    News = models.ForeignKey(news, on_delete= models.CASCADE)
    image = models.ImageField(upload_to='images/',blank = True, null= True)

    def __str__(self):
        return '%s' % (self.News)

class TagsNValue(models.Model):
    tags = models.CharField(max_length=240, db_index=True)
    value = models.IntegerField(db_index=True)
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return '%s' % (self.name+' '+self.tags+' '+str(self.value))

class HeadlineNews(models.Model):
    news_id = models.ForeignKey(news, on_delete= models.CASCADE,related_name='news')