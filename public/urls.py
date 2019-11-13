from django.urls import path, include
from public import views
from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register('users', views.PublicUserViewSet, base_name='users')


urlpatterns = [
    path('v1/', include(router.urls)),
]
