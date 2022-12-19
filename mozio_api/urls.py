from django.urls import path
from mozio_api.views import Provider, ProviderDetail, ServiceArea, ServiceAreaDetail

urlpatterns = [
    path('providers/', Provider.as_view()),
    path('providers/<str:pk>', ProviderDetail.as_view()),
    path('servicearea/', ServiceArea.as_view()),
    path('servicearea/<str:pk>', ServiceAreaDetail.as_view()),
   
]