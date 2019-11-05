from django.urls import path
from .views import LoginView, TokenInfoView



urlpatterns = [
    path('v1/login/', LoginView.as_view(), name='login'),
    path('v1/info/', TokenInfoView.as_view(), name='info')
]