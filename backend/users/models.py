from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта', unique=True, blank=False, max_length=150)
    first_name = models.CharField('Имя', blank=False, max_length=50)
    last_name = models.CharField('Фамилия', blank=False, max_length=50)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
