from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import MyTokenObtainPairView, message_view, message_list, posts_view, logout_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    # Path to obtain a new access and refresh token
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Submit your refresh token to this path to obtain a new access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/messages/<int:sender>/<int:receiver>', message_view, name='message_view'),
    path('api/messageslist/<int:user>', message_list, name='message_list'),
    path('api/miestnost/<int:miestnost>', posts_view, name='message_list'),
    path('api/logout/', logout_view, name='logout')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
