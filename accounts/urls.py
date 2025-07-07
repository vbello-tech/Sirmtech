from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from .views import HomeView,  CatalogueView

app_name = "user"
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('catalogue/', CatalogueView.as_view(), name="catalogue"),
    path('login/', LoginView.as_view(template_name='registrations/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]