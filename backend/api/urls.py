from django.urls import path
from .views import *

urlpatterns = [
    path('predict/', PredictPlanet.as_view()),
    path('planets/', PlanetList.as_view()),
    path('stars/', StarList.as_view()),
    path('stars/<int:star_id>/planets/', StarPlanetList.as_view(), name='star-planet-list'),
]
