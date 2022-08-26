from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from dashboard import views as  dash_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("dashboard.urls", namespace="dashboard")),
    path("register/", dash_views.CreateUserView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
] + static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#   urlpatterns += static(
#     settings.MEDIA_URL, 
#     document_root=settings.MEDIA_ROOT)