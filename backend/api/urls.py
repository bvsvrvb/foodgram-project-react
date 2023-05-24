from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

# api/users - get, post - 'djoser.urls'
# api/users/id - get
# api/users/me - get
# api/users/set_password/ - post
# api/auth/token/login/ - +
# api/auth/token/logout/ - +