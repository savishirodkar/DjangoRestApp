from home.views import index, people, login, PersonAPI, PeopleViewSet, RegisterAPI, LoginAPI
from django.urls import path, include

#Router
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='person')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('index/', index),
    path('person/', people),
    path('login/', login),
    path('person-api/', PersonAPI.as_view())

]