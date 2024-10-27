from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView, DeleteUserView, UserRetrieveUpdateView, google_login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # authentication
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name='register'),
    path('api/user/delete/', DeleteUserView.as_view(), name='delete'),
    # path('api/user/details/', UserDetailsView.as_view(), name='details'),
    path('api/user/details/', UserRetrieveUpdateView.as_view(), name='details'),
    path('api/token/', TokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api-auth/', include('rest_framework.urls')),
    # path for api/urls.py (listing create/delete)
    path("api/", include("api.urls")),
    path('accounts/', include('allauth.urls')),  # Allauth routes
    # google login endpoint
    path('api/google-login/', google_login, name='google_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
