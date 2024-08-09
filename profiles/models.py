from addresses.models import Address
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        try:
            return self.user.get_full_name()
        except:
            return self.user.phone.as_e164

    # custom functions
    def get_absolute_url(self):
        try:
            url = reverse("profiles:profile")
        except:
            url = '#get_absolute_url'
        return url

    def get_update_url(self):
        try:
            url = reverse("profiles:profile_update")
        except:
            url = '#get_update_url'
        return url
