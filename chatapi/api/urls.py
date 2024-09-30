from django.urls import path, include
from rest_framework.authtoken import views

from .views import MessageListCreateAPIView

urlpatterns = [
    path('messages/', MessageListCreateAPIView.as_view(), name='message-list'),
    path('auth/', include('rest_auth.urls')),
    path('token/', views.obtain_auth_token),
]
