from django.urls import path, reverse_lazy
from . import views

from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.register_user, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('password-change', views.password_change, name='password_change'),
    path('reset_password/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('account:password_reset_done')), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="reset_password_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="reset_password_complete"),

    path('profile/', views.profile, name="profile"),

]