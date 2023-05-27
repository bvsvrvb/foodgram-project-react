from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .pagination import CustomPageNumberPagination
from .serializers import SubscriptionSerializer
from users.models import User

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
