from rest_framework import routers

from core.views import CategoryViewSet, ProductViewSet, PriceViewSet

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"prices", PriceViewSet, basename="prices")

urlpatterns = [*router.urls]
