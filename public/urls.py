from django.urls import path, include
from public import views
from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register('users', views.PublicUserViewSet, base_name='users')
router.register('competitions', views.PublicCompetitionViewSet, base_name='competitions')

competition_router = routers.NestedSimpleRouter(router, 'competitions', lookup='competition')
competition_router.register('participants', views.ParticipantsViewSet, basename='public-competition-participants')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(competition_router.urls))
]
