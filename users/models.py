from django.contrib.auth.models import AbstractUser
from django.db import models


class RoleUser(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):

    email = models.EmailField(unique=True, blank=False)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=10,
        choices=RoleUser.choices,
        default=RoleUser.USER
    )

    @property
    def is_admin(self):
        return (self.role == RoleUser.ADMIN or self.is_staff
                or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == RoleUser.MODERATOR
