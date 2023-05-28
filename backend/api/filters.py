import django_filters

from recipes.models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
