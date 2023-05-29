from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from .pagination import CustomPageNumberPagination
from . import serializers, filters, permissions
from users.models import User, Follow
from recipes.models import Tag, Recipe, Ingredient, Favorite

ALLOWED_USER_METHODS = ('get', 'post', 'delete')
ALLOWED_METHODS = ('get', 'post', 'patch', 'delete',
                   'head', 'options', 'trace')


class CustomUserViewSet(UserViewSet):
    http_method_names = ALLOWED_USER_METHODS
    pagination_class = CustomPageNumberPagination

    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        pagination_class=CustomPageNumberPagination
    )
    def subscriptions(self, request, *args, **kwargs):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = serializers.SubscriptionSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
        pagination_class=CustomPageNumberPagination
    )
    def subscribe(self, request, *args, **kwargs):
        followed_user = get_object_or_404(User, pk=self.kwargs.get('id'))
        serializer = serializers.FollowSerializer(
            data={'user': request.user.id, 'following': followed_user.id},
            context={'request': request}
            )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            try:
                subscription = get_object_or_404(
                    Follow, user=request.user, following=followed_user)
            except Http404:
                raise ValidationError({'errors': 'Вы не подписаны'})
            subscription.delete()
            return Response(
                f'Вы отписались от {followed_user}',
                status=status.HTTP_204_NO_CONTENT
            )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ALLOWED_METHODS
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (permissions.AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.RecipeSerializer
        return serializers.CreateRecipeSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        serializer = serializers.FavoriteSerializer(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
            )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                favorite = get_object_or_404(
                    Favorite, user=request.user, recipe=recipe)
            except Http404:
                raise ValidationError({'errors': 'Рецепта нет в избранном'})
            favorite.delete()
            return Response(
                'Рецепт удален из избранного',
                status=status.HTTP_204_NO_CONTENT
            )
