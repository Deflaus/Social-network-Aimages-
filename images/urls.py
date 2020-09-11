from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('', views.images_list, name='list_images'),
    path('addingimage/', views.adding_image, name='addingimage'),
    path('like/', views.image_like, name='like'),
    path('detail/<int:id>/', views.image_detail, name='detail'),
    path('feed/', views.feed, name='feed')
]
