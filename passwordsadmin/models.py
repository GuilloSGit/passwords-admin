from django.db import models
from django.contrib.auth.models import User

class Password(models.Model):
    name         = models.CharField(max_length=50)
    url          = models.CharField(max_length=100, blank=True)
    password     = models.CharField(max_length=25)
    passwordTag  = models.CharField(max_length=15, blank=True)
    dateSaved    = models.DateTimeField(auto_now_add=True)
    shared       = models.BooleanField(default=False, blank=True)
    sharedWith   = models.ManyToManyField(User, related_name='shared_passwords', blank=True)
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_passwords')
    active       = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.shared:
            self.sharedWith.clear()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name