from django.urls import path, include
from notify import views

urlpatterns = [
    path('notifications/', views.notification_list),
    path('notification/<int:pk>/', views.notification_detail)
]

