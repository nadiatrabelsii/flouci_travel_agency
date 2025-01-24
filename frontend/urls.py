from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    path('book/<int:package_id>/', views.book_package, name='book_package'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('package/<int:package_id>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('news/', views.news_page, name='news_page'),
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('chatbot/response/', views.chatbot_response, name='chatbot_response'),
]
