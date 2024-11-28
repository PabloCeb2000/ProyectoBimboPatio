from rest_framework import routers
from django.urls import path, include
from .views import ProductViewSet, TruckViewSet, OutGoingOrderViewSet, ActiveStockViewSet, ReserveStockViewSet, StockOBLPNViewSet, RemissionViewSet, PendingViewSet, TruckUnloadingView, TruckDepartureView, TruckArrivalView

router = routers.DefaultRouter()

# Register ViewSets (automatic CRUD functionality)
router.register(r'products', ProductViewSet)
router.register(r'trucks', TruckViewSet)
router.register(r'outgoing-orders', OutGoingOrderViewSet)
router.register(r'active-stocks', ActiveStockViewSet)
router.register(r'reserve-stocks', ReserveStockViewSet)
router.register(r'stock-oblpn', StockOBLPNViewSet)
router.register(r'remissions', RemissionViewSet)

# Register other specific viewsets with basenames
router.register(r'pendings', PendingViewSet, basename='pending') 

router.register(r'truck-arrival', TruckArrivalView, basename='retrieve-remission')
router.register(r'unloading-trucks', TruckUnloadingView, basename="unloading-trucks")
router.register(r'truck-departure', TruckDepartureView, basename="truck-departure")

urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the router
   
]
