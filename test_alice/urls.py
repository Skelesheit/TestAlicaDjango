from django.urls import include, path
from rest_framework.routers import DefaultRouter

from test_alice import views

router = DefaultRouter()

router.register('webhook', views.AliceGame, basename='webhook')
urlpatterns = [
    path('', include(router.urls))
]
