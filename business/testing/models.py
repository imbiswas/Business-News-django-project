from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=400)
    def __str__(self):
        return '%s' % (self.title)

def get_image_filename(instance, filename):
    id = instance.post.id
    return "post_images/%s" % (id)  


class Images(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')

    def __str__(self):
        return '%s' % (self.post)