from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'prediction'

urlpatterns = [
    path("", views.dashboard, name= "dashboard"),
    path('predict/', views.predict_image, name='predict_image'),
    path('result/<int:prediction_id>/', views.result, name='result'),
]

