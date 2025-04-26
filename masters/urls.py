from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, PartViewSet

# DRFのルーターを設定
router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet, basename="supplier")
router.register(r"parts", PartViewSet, basename="part")

# 将来的に他のマスタモデルも追加可能

urlpatterns = [
    path("", include(router.urls)),
]
