from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=50,
        blank=False,
        db_index=True
        )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=50,
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
        max_length=50,
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
        max_length=50,
        blank=False,
        db_index=True
        )
    image = models.ImageField('Изображение', upload_to='recipes/', blank=False)
    text = models.TextField('Описание', blank=False)
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        verbose_name='Ингредиенты',
        related_name='recipes'
        )  # choises
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        verbose_name='Теги',
        related_name='recipes'
        )  # choises
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        blank=False
        )  # validators=[validate_cooking_time] - время в минутах?

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique_author_recipe'
            ),
        ]

    def __str__(self):
        return self.name


class RecipeTags(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.recipe} {self.tags}'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    ingredients = models.ForeignKey(
        Ingredient, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveSmallIntegerField(
        'Количество',
        blank=False,
        default=0
        )

    def __str__(self):
        return f'{self.recipe} {self.ingredients}'


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

    def __str__(self):
        return f'{self.user} {self.recipe}'
