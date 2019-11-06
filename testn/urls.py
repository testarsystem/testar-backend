from django.urls import path, include
from .views import TestViewSet
from rest_framework_nested import routers


router = routers.SimpleRouter()

router.register('tests', TestViewSet, base_name='tests')



urlpatterns = [
    path('v1/', include(router.urls)),
]
