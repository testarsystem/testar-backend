from django.urls import path, include
from competition import views
from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register('competitions', views.CompetitionViewSet, base_name='competitions')


competitions_router = routers.NestedSimpleRouter(router, 'competitions', lookup='competition')
competitions_router.register('participants', views.ParticipantsViewSet, basename='competitions-participants')
#
# questions_router = routers.NestedSimpleRouter(tests_router, 'questions', lookup='question')
# questions_router.register('answers', views.AnswerViewSet, basename='question-answers')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(competitions_router.urls)),
    # path('v1/', include(questions_router.urls))
]
