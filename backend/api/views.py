from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from djoser.serializers import SetPasswordSerializer
from djoser import views

from users.models import User
from .serializers import UserSerializer


class UserViewSet(views.UserViewSet):
    pass


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     @action(methods=['get'], detail=False,
#             permission_classes=[IsAuthenticated])
#     def me(self, reguest):
#         serializer = self.get_serializer(reguest.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @action(['post'], detail=False,
#             permission_classes=[IsAuthenticated])
#     def set_password(self, request):
#         serializer = SetPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.request.user.set_password(serializer.data['new_password'])
#         self.request.user.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def subscribe(self, reguest):
#         pass

#     def subscriptions(self, reguest):
#         pass
