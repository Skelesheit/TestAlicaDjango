from django.urls import path

from rest_framework.routers import DefaultRouter

from test_alice import views

router = DefaultRouter()

router.register(r'webhook', views.AliceWebhookHi, basename='alice')

urlpatterns = router.urls