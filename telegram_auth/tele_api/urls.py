from django.urls import path
from .views import telegram_auth, telegram_callback

urlpatterns = [
    path('auth/', telegram_auth, name='telegram_auth'),
    path('auth/complete/telegram/', telegram_callback, name='telegram_callback'),
]
