from django.urls import path, include
from home.views import index , person, login, PersonAPI, PeopleViewSet, RegisterAPI, LoginAPI
 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('index/', index ),
    path('person/', person ),
    path('login/', LoginAPI.as_view() ),
    path('persons/', PersonAPI.as_view() ),
    path('register/', RegisterAPI.as_view() ),
]
    
