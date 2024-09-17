from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.tweet_list,name='tweet_list'),
    path('create/', views.tweet_create,name='tweet_create'),
    path('<int:tweet_id>/delete/', views.tweet_delete,name='tweet_delete'),
    path('<int:tweet_id>/edit/', views.tweet_edit,name='tweet_edit'),
    path('register/', views.register,name='register'),
    path('search/', views.tweet_search, name='tweet_search'),  # Search URL


    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
     path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',
             success_url='/reset/done/'),  # Custom success URL
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]