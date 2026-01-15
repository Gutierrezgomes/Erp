from django.urls import path
from financeiro.views import fina_view
from . import views


urlpatterns = [
    path('', fina_view, name= 'home'),
    path('categorias/', views.catego_view, name='categorias'),
    path('lancamentos/', views.lanca_view, name='lancamentos'),
]