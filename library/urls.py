from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'loans', views.LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Authentication endpoints
    path('auth/login/', views.login_view, name='auth_login'),
    path('auth/register/', views.register_view, name='auth_register'),
    path('auth/logout/', views.logout_view, name='auth_logout'),
    path('auth/me/', views.me_view, name='auth_me'),
    path('auth/profile/', views.profile_view, name='auth_profile'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]