from django.db import models
from django.contrib.auth.models import AbstractUser
from tokens.models import MultiToken

class Base(models.Model):
    """
    Base class will have the row level create and update logs
    """
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def created_date(self):
        return self.created_on.strftime("%d %b %Y").upper()

    def created_date_time(self):
        return self.created_on.strftime("%d-%m-%Y %H:%M:%S")

    def updated_date(self):
        return self.updated_on.strftime("%d %b %Y").upper()

    def updated_date_time(self):
        return self.updated_on.strftime("%d-%m-%Y %H:%M:%S")


class User(AbstractUser):

    class Meta(AbstractUser.Meta):
        AbstractUser._meta.get_field('first_name').max_length = 255
        AbstractUser._meta.get_field('last_name').max_length = 255
        AbstractUser._meta.get_field('first_name').required = True
        AbstractUser._meta.get_field('last_name').required = False
        AbstractUser._meta.get_field('email').required = False
        AbstractUser._meta.get_field('email').null = True

    def __str__(self):
        return "%s, %s" % (self.username if self.username else 'No Name', self.first_name)

    def get_auth_token(self):
        return "Token " + MultiToken.objects.create(user_id=self.id).key

    def delete_auth_token(self, key):
        MultiToken.objects.filter(key=key).delete()
