from typing import Optional

from django.db import models

from users.models import User


class RecipeQuerySet(models.QuerySet):
    def add_user_annotations(self, user_id: Optional[int]):
        return self.annotate(
            in_shopping_cart=models.Exists(
                Cart.objects.filter(
                    user_id=user_id, recipe__pk=models.OuterRef('pk')
                )
            ),
            in_favorite=models.Exists(
                Favorite.objects.filter(
                    user_id=user_id, recipe__pk=models.OuterRef('pk')
                )
            )
        )


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=150,
        blank=False,
        db_index=True
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=150,
        blank=False
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=150,
        blank=False,
        unique=True,
        db_index=True
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        blank=False,
        unique=True,
        default="#ffffff"
    )
    slug = models.SlugField(blank=False, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    objects = RecipeQuerySet.as_manager()
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='recipes',
        blank=False,
        null=True,
        verbose_name='Автор'
    )
    name = models.CharField(
        'Название',
        max_length=200,
        blank=False,
        db_index=True
    )
    image = models.ImageField('Изображение', upload_to='recipes/', blank=False)
    text = models.TextField('Описание', blank=False)
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        verbose_name='Теги',
        related_name='recipes',
        through='RecipeTag'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        blank=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique_author_recipe'
            ),
        ]

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, null=True)
    amount = models.PositiveSmallIntegerField(
        'Количество',
        blank=False,
        default=0
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return f'{self.user} {self.recipe}'
