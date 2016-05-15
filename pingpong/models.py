from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # links user model to associated models
    user = models.OneToOneField(User)
    # adding associated model for additional fields
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # override unicode method
    def __unicode__(self):
        return self.user.username
