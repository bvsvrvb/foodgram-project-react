from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта', unique=True, blank=False, max_length=150)
    first_name = models.CharField('Имя', blank=False, max_length=50)
    last_name = models.CharField('Фамилия', blank=False, max_length=50)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_follow'
            ),
        ]

    def __str__(self) -> str:
        return f'{self.user} {self.following}'
