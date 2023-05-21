from django.contrib import admin

from .models import Recipe, Tag, Ingredient, Favorite


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('name', 'author', 'tags')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_filter = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
