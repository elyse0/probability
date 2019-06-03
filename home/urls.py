from django.urls import path
from home.views import *

urlpatterns = [

    path('', HomeView.as_view()),
    path('distribucion-probabilidad-conjunta', ProbabilidadConjuntaView.as_view()),
    path('probabilidad-distribucion-conjunta', ProbabilidadDensidadConjuntaView.as_view()),
    path('probabilidad-continua', ProbabilidadContinuaView.as_view()),
    path('funcion-acumulativa-continua', AcomulativaContinuaView.as_view()),
    path('valor-esperado-continua', EsperadoContinuaView.as_view()),
    path('varianza-continua', VarianzaContinuaView.as_view())
]