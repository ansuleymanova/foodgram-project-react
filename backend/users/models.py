from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    email = models.EmailField(unique=True)

    @property
    def is_admin(self):
        return self.is_staff


class Subscription(models.Model):
    subscriber = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='subscriber')
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='subscriptions')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'author'],
                                    name='unique_subscription')]
