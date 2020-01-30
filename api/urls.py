from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from api.views import PouzivatelViewSet, SpravaViewSet, MiestnostViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'users', PouzivatelViewSet)
router.register(r'messages', SpravaViewSet)
router.register(r'miestnosti', MiestnostViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
]