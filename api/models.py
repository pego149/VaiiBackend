from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.cache import cache
import datetime


class Pouzivatel(AbstractUser):
    def __str__(self):
        return self.username

    def last_seen(self):
        return cache.get('last_seen_%s' % self.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else:
            return False


class PouzivatelProfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(blank=True, max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    photo = models.ImageField(upload_to='img', null=True)


class Sprava(models.Model):
    odosielatel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='odosielatel')
    prijmatel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prijmatel')
    sprava = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sprava

    class Meta:
        ordering = ('timestamp',)


class Miestnost(models.Model):
    nazov = models.CharField(max_length=100)

    def __str__(self):
        return self.nazov


class Post(models.Model):
    odosielatel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='odosielatelPost')
    miestnost = models.ForeignKey(Miestnost, on_delete=models.CASCADE, related_name='miestnost')
    sprava = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sprava

    class Meta:
        ordering = ('timestamp',)
