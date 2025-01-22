from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from travel_app.views import UserViewSet, PackageViewSet, BookingViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
