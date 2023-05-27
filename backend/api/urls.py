from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

# api/users - get, post / allowany
# api/users/{id} - get / allowany
# api/users/me - get
# api/users/set_password/ - post

# api/users/{id}/subscribe - post, delete
# api/users/subscriptions - get