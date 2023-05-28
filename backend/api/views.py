from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404

from .pagination import CustomPageNumberPagination
from .serializers import SubscriptionSerializer, FollowSerializer
from users.models import User, Follow

ALLOWED_METHODS = ('get', 'post', 'delete')


class CustomUserViewSet(UserViewSet):
    http_method_names = ALLOWED_METHODS
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
        serializer = SubscriptionSerializer(
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
        serializer = FollowSerializer(
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
