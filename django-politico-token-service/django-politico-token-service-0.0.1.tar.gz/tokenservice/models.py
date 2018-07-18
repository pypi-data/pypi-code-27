import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class TokenApp(AbstractBaseUser):
    """
    Becuase DRF expects authentication classes to return a User instance,
    we use AbstractBaseUser to fake one.
    """
    app_name = models.SlugField(max_length=100, unique=True)
    token = models.SlugField(max_length=30, unique=True, editable=False)
    password = None
    last_login = None

    USERNAME_FIELD = 'app_name'

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex[:30]
        super().save(*args, **kwargs)
