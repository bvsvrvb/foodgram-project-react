import django_filters
from django_filters import filters
from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.NumberFilter(method='get_favorited')
    is_in_shopping_cart = filters.NumberFilter(method='get_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_favorited(self, queryset, name, value):
        queryset.add_user_annotations(self.request.user.id)
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorited__user=self.request.user)
        return queryset

    def get_in_shopping_cart(self, queryset, name, value):
        queryset.add_user_annotations(self.request.user.id)
        if value and self.request.user.is_authenticated:
            return queryset.filter(cart__user=self.request.user)
        return queryset
