from django.urls import path, include
from .views import LoginView, TokenInfoView, RegistrationViewSet
from rest_framework_nested import routers


router = routers.SimpleRouter()

router.register('registration', RegistrationViewSet, base_name='registration')


urlpatterns = [
    path('v1/login/', LoginView.as_view(), name='login'),
    path('v1/info/', TokenInfoView.as_view(), name='info'),
    path('v1/', include(router.urls)),
]