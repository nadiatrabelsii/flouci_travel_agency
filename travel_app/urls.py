from django.urls import path
from . import views
from .views import api_recommendations

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    path("news/", views.news_page, name="news_page"),
    path('api/recommendations/<str:user_id>/', api_recommendations, name='api_recommendations'),
]