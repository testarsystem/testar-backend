from django.urls import path, include
from testn import views
from rest_framework_nested import routers


router = routers.SimpleRouter()

router.register('tests', views.TestViewSet, base_name='tests')


tests_router = routers.NestedSimpleRouter(router, 'tests', lookup='test')
tests_router.register('questions', views.QuestionViewSet, basename='tests-questions')

questions_router = routers.NestedSimpleRouter(tests_router, 'questions', lookup='question')
questions_router.register('answers', views.AnswerViewSet, basename='question-answers')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(tests_router.urls)),
    path('v1/', include(questions_router.urls))
]
