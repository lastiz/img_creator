from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('add/', views.AddImageView.as_view(), name='add'),
    path('change_done/<int:pk>/<path:new_img_url>/', views.ChangeDoneView.as_view(), name='change_done'),
    path('detail/<int:pk>/', views.detail, name='detail'),
]
