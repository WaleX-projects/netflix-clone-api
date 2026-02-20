from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MovieViewSet, ProfileViewSet, UserAccountView

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'user-profiles', ProfileViewSet, basename='user-profiles')

urlpatterns = [
    # Auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Account Info
    path('api/account/', UserAccountView.as_view(), name='user_account'),
    
    # Movies and Netflix-Profiles
    path('', include(router.urls)),
]
