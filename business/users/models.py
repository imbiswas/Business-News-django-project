from django.db import models
from django.contrib.auth.models import User
from .choices import *

class UserData(models.Model):

    userID = models.CharField(max_length = 100)
    newsID = models.CharField(max_length = 100)



    # class Meta:
    #   ordering = ["-timestamp"]

    def __str__(self):

        return self.userID + self.newsID

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})